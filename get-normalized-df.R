# Title     : TODO
# Objective : TODO
# Created by: Stian
# Created on: 08/03/2021
library(vegan)
args <- commandArgs(trailingOnly = TRUE)

csv.path <- args[1]

# print(csv.path)

fov.n.lok <- read.csv(csv.path)

rownames(fov.n.lok) <- fov.n.lok$Sample # sets the index to the sample names

atr.all <- subset(fov.n.lok, select = -Sample) # Removes the sample column, leaving only the index and the data

atr <- subset(atr.all, select = -Total) # removes the total column
atr.norm <- decostand(atr, 'total')
write.csv(atr.norm, "normalized_df.csv", row.names = TRUE)
cat("normalized_df.csv")



