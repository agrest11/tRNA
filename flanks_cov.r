library(ggplot2)
library(reshape2)
library(ggpubr)
library(reticulate)
library(dplyr)

duplikaty <- read.csv("/home/aga/Pulpit/magisterka/dane_filtr/blast/arvense/blast-arvense.csv", 
                      header = TRUE, sep = ",")

filtrowane <- duplikaty[duplikaty$query_coverage >= 70 & 
                        duplikaty$found_length >= 70,
                        c("query_id", "found_id", "identities",
                          "found_length", "query_begin", "query_end",
                          "found_begin", "found_end",
                          "score", "query_coverage")]

grupowane <- count(filtrowane, query_id)
grupowane <- grupowane[grupowane$n > 1, c("query_id", "n")]
rownames(grupowane) <- NULL
grupowane
sum(grupowane$n)

ggplot(grupowane, aes(x=query_id, y=n)) +
  theme_bw() +
  geom_bar(stat="identity", fill="lightgreen") +
  ggtitle("Liczba powtórzeń genów u T. arvense") +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(angle = 45, vjust = 1, hjust=1),
        plot.margin = margin(10, 10, 10, 30)) +
  xlab("identyfikator sekwencji") + 
  ylab("liczba powtórzeń")
ggsave("/home/aga/Pulpit/wykresy7/t-arvense-powtórzenia.png", width = 10, height = 6)

dane <- read.csv("/home/aga/Pulpit/magisterka/dane_filtr/blast/t-arvense.csv", 
                 header = TRUE, sep = ",")

filtr <- dane[dane$left_flank >= 60 | dane$right_flank >= 60 & dane$gene >= 60, 
              c("query_id", "found_id", "left_flank", "right_flank",
                "gene", "score", "query_coverage")]
rownames(filtr) <- NULL

dfm <- melt(filtr[,c('query_id', 'left_flank','gene','right_flank')],
            id.vars = 1)

ggplot(dfm,aes(x = query_id,y = value)) + 
  theme_bw() +
  geom_col(aes(fill = variable),
           position = position_dodge(0.5), width = 0.5) + 
  ggtitle("Rozkład pokrycia sekwencji flankujących i genów dla T. arvense") +
  theme(plot.title = element_text(hjust = 0.5), legend.title=element_blank(),
        axis.text.x = element_text(angle = 45, vjust = 1, hjust=1),
        plot.margin = margin(10, 10, 10, 30)) +
  xlab("identyfikator sekwencji") + 
  ylab("% pokrycia") +
  scale_fill_manual(values = c("lightgreen","lightgray", "darkgray"),
                    labels=c('lewa flanka', 'gen', 'prawa flanka')) +
  scale_x_discrete(guide = guide_axis(check.overlap = TRUE))
ggsave("/home/aga/Pulpit/wykresy7/t-arvense-flanki.png", width = 10, height = 6)

ggscatter(dane, x = "score", y = "query_coverage", 
          add = "reg.line", cor.method = "pearson",
          xlab = "punktacja BLASTa", ylab = "% pokrycia",
          title = "Korelacja % pokrycia i punktacji BLASTa dla T. arvense") +
  theme(plot.title = element_text(hjust = 0.5))
ggsave("/home/aga/Pulpit/wykresy7/t-arvense-korelacja.png", width = 10, height = 6)

x <- dane$query_coverage
png(file="/home/aga/Pulpit/wykresy7/t-arvense-pokrycie.png",
    width=600, height=350)
hist(x, breaks=10, col="lightgreen", xlab="% pokrycia",
        ylab="częstość",
        main="Rozkład % pokrycia dla T. arvense")
xfit<-seq(min(x),max(x),length=40)
yfit<-dnorm(xfit,mean=mean(x),sd=sd(x))
yfit <- yfit*diff(h$mids[1:2])*length(x)
lines(xfit, yfit, col="blue", lwd=2)
dev.off()
