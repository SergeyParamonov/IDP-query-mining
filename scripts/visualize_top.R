library(reshape2)
library(ggplot2)
source("scripts/auxiliary_visualization_functions.R")

data <- read.csv("results/top/raw", header=TRUE, stringsAsFactors=FALSE)
visual <- ggplot(data, aes(x=dataset, y=runtime, colour=dataset)) 
visual <- visual + geom_boxplot(se=FALSE, size=1.3) +  theme_bw()
visual <- visual + scale_y_continuous("Runtime in seconds", limits=c(0,50000)) + scale_x_discrete("") # two points outside 
ggsave(visual,file="figure_top_one_experiment.pdf")
print(visual)
