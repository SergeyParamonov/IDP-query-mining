library(reshape2)
library(ggplot2)
source("scripts/auxiliary_visualization_functions.R")

#reading data
mutagenesis <- scan("results/enumeration/mutagenesis")
toxinology  <- scan("results/enumeration/toxinology")
yoshida     <- scan("results/enumeration/yoshida")
nctrer      <- scan("results/enumeration/nctrer")
bloodbarr   <- scan("results/enumeration/bloodbarr")
enzymes     <- scan("results/enumeration/enzymes")

df <- data.frame(pattern_index=seq_along(mutagenesis), bloodbarr, mutagenesis, nctrer, toxinology, yoshida, enzymes)
long_df <- melt(df, id="pattern_index")

visual <- ggplot(long_df, aes(x=pattern_index, y=value, colour=variable))
visual <- visual + geom_smooth(se=FALSE, size=1.3) + geom_point() + theme_bw()
visual <- visual + scale_x_continuous("i-th iteration") + scale_y_continuous("Runtime in seconds", limits=c(0,230)) + scale_color_manual(values=get_colors(), guide = guide_legend(title = "dataset"))
ggsave(visual,file="figure_enumeration_experiment.pdf")
print(visual)
