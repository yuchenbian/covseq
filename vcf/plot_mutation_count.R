library(data.table)
library(ggplot2)
library(cowplot)

in_fn = "../processed_data/vcf/filter_samples/mutation_count.tsv"
out_dir = "../processed_data/vcf/plot_mutation_count/"
if (!dir.exists(out_dir)) {dir.create(out_dir)}

mutation_count = fread(in_fn, sep="\t", col.names=c("sample", "mutation"))
p = ggplot(mutation_count, aes(x=mutation)) + 
	geom_histogram(bins=80) + 
	scale_y_sqrt(breaks=c(1,50,500,1000,1500,2000)) + 
	scale_x_log10(breaks=c(1,10,100,150,1000,10000), labels=c(1,10,"100   ","   150",1000,10000)) + 
	geom_vline(xintercept=150, color="red", linetype="dashed") + 
	xlab("Number of mutations in sample") + 
	ylab("Frequency")
print(p)
save_plot(sprintf("%s/mutation_count.pdf", out_dir), p, base_height=4, base_width=6)