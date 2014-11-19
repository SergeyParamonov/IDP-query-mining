library(reshape2)
library(ggplot2)

data <- read.csv("results/top/raw", header=TRUE, stringsAsFactors=FALSE)
visual <- ggplot(data, aes(x=dummy_index, y=runtime, colour=dataset)) 
visual <- visual + geom_smooth(se=FALSE, size=1.3) + geom_point() + theme_bw()
visual <- visual + scale_x_continuous("pattern index") + scale_y_continuous("Runtime in seconds") + scale_colour_discrete("") 
ggsave(visual,file="figure_top_one_experiment.pdf")
print(visual)
