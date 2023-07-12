library(ggplot2)

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("ggtree")

install.packages("ragg")

install.packages("devtools", dependencies = TRUE)
devtools::install_github("thackl/thacklr")
devtools::install_github("thackl/gggenomes")

df_main <- read.csv("/home/aga/Pulpit/magisterka/dane_filtr/blast-alpina-filtr.csv", 
                    header = TRUE, sep = ",")

genes <- df_main[,c(1, 9, 10)]
seqs <- df_main[,c(1, 4)]
links <- df_main[,c(1, 2)]

gggenomes(genes, seqs, links)
