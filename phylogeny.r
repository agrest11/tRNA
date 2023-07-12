library(tidyverse)
library(ggtree)

tree <- read.tree("tree.nwk")
tree
ggplot(tree) + geom_tree() + theme_tree()
ggtree(tree) + geom_nodepoint() + geom_tiplab() + ggplot2::xlim(0,4)
ggsave("/home/aga/Pulpit/wykresy7/phylogeny.png", width = 10, height = 6)
