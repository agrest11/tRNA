#! /bin/bash

#puszczenie skryptu do zrobienia sekwencji z flankami
<<com
for directory in $(ls -d */); do echo "$directory"; filefasta=($directory/*.fna); filess=($directory/trnascan/2*.ss); 
python3 1-trna-genes.py $filefasta $filess $directory; done
com

#sprawdzenie
<<com
for directory in $(ls -d */); do echo "$directory"; fileout=($directory/trnascan/4*.ss); 
python3 test-trna-genes.py $fileout; done
com

#puszczenie algorytmu do znalezienia klastrów
<<com
for directory in $(ls -d */); do echo "$directory"; fileout=($directory/trnascan/2*.out); 
python3 2-clusters2.py $fileout $directory; done
com

#puszczenie algorytmu do znalezienia takich samych klastrów u różnych organizmów
<<com
for directory1 in $(ls -d */)
do for directory2 in $(ls -d */)
do if [ $directory1 != $directory2 ]
then
  	echo "$directory1"
  	echo "$directory2"
	filecluster1=($directory1/*clusters.txt)
	filecluster2=($directory2/*clusters.txt)
	python3 3-compare2.py $filecluster1 $filecluster2 > wynik.txt
	python3 4-check.py $directory1 $directory2
fi
rm filtr*.txt
rm wynik.txt
done
done
mkdir compared
mv *-vs-*.txt compared/
mv next.py compared/
com

<<com
cd compared
for file in $(ls *.txt); do python3 next.py $file; done
com

<<com
for directory in $(ls -d */); do echo "$directory"; filefasta=($directory/*.fna); python3 filtr.py $filefasta; done
com

<<com
for directory in $(ls -d */); do echo "$directory"; file=($directory/*clusters.txt); python3 5-clusters-in-org.py $file >> c.txt; done
com

<<com
for directory in $(ls -d */); do echo "$directory"; file=($directory/*clusters-ids.txt); file2=($directory/*flanks.txt); 
python3 7-get-single-trnas.py $file $file2; done
com

<<com
for directory in $(ls -d */); do echo "$directory"; file=($directory/trnascan/2*.ss); python3 8-count-contigs.py $file >> contigs.txt; done
com


for directory in $(ls -d */); do
file=($directory/*.csv); 
if test -f "$file"; then
    echo "$directory"
    python3 9-synteny.py $file
fi; 
done
