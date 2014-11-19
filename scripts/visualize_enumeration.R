library(reshape2)
library(ggplot2)

#reading data
mutagenesis <- scan("results/enumeration/mutagenesis")
toxinology  <- scan("results/enumeration/toxinology")
yoshida     <- scan("results/enumeration/yoshida")
nctrer      <- scan("results/enumeration/nctrer")
bloodbarr   <- scan("results/enumeration/bloodbarr")
enzymes     <- scan("results/enumeration/enzymes")

df <- data.frame(pattern_index=seq_along(mutagenesis), mutagenesis, toxinology, yoshida, nctrer, bloodbarr, enzymes)
long_df <- melt(df, id="pattern_index")

visual <- ggplot(long_df, aes(x=pattern_index, y=value, colour=variable)) 
visual <- visual + geom_smooth(se=FALSE, size=1.5) + geom_point() + theme_bw()
visual <- visual + scale_x_continuous("i-th iteration") + scale_y_continuous("Runtime in seconds", limits=c(0,230)) + scale_colour_discrete("") 
ggsave(visual,file="figure_enumeration_experiment.pdf")
print(visual)
