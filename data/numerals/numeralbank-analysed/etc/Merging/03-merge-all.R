#load libraries----
library(tidyverse)
options(tidyverse.quiet = TRUE)

#set working directory and load data----
#setwd(getSrcDirectory()[1]) # run this line if using plain R
setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) #run this line if using RStudio

#Visualize NumValue as non-scientific notation
options(scipen = 1000000000)

#load and merge data

all.data <- NULL





data.glossed.checked <- read.csv("../glossed/all.data.checked.csv")
data.reglossed.checked <- read.csv("../re-glossed/all.data.checked.csv",row.names = 1)
doculects.good <- read.csv("../doculects.to.use.in.analyses_20260916.csv")

data.glossed <- read.csv("../glossed/all.data.glossed.csv")
data.reglossed<- read.csv("../re-glossed/all.data.glossed.csv",row.names = 1)

data.glossed.merged <- rbind(data.glossed,
                     data.reglossed)

data.glossed.checked.merged <- rbind(data.glossed.checked,
                             data.reglossed.checked)

length(unique(data.glossed.merged$FileName))
length(unique(data.glossed.checked.merged$FileName))
# 6155 doculects in merged
# 6097 doculects in checked
write.csv(data.glossed.merged, "data.glossed.merged.csv")
write.csv(data.glossed.checked.merged, "data.glossed.checked.merged.csv")



data.glossed.merged %>%
  left_join(doculects.good, join_by(FileName == File)) %>% 
  filter(Use_in_analyses == "YES") -> data.glossed.merged.filtered

data.glossed.checked.merged %>%
  left_join(doculects.good, join_by(FileName == File)) %>% 
  filter(Use_in_analyses == "YES") -> data.glossed.checked.merged.filtered
  
table(doculects.good$Use_in_analyses)

length(unique(data.glossed.merged.filtered$FileName))
length(unique(data.glossed.checked.merged.filtered$FileName))
# 5048 doculects should be filtered
# 4990 doculects are checked and filtered
write.csv(data.glossed.merged.filtered, "data.glossed.merged.filtered.csv")
write.csv(data.glossed.checked.merged.filtered, "data.glossed.checked.merged.filtered.csv")

#check mismatches between glossed and checked

data.glossed.merged %>%
  filter(!(ID %in% data.glossed.checked.merged$ID)) -> problematic.full


data.glossed.merged.filtered %>%
  filter(!(ID %in% data.glossed.checked.merged.filtered$ID)) -> problematic.filtered

data.glossed.checked.merged %>%
  filter(!(ID %in% data.glossed.merged$ID))
data.glossed.checked.merged.filtered %>%
  filter(!(ID %in% data.glossed.merged.filtered$ID))

# colnames(data.glossed)
# colnames(data.glossed.checked)
# anti_join(data.glossed,data.glossed.checked[1:18]) -> problematic.full
# anti_join(data.glossed.filtered,data.glossed.checked.filtered[1:18]) -> problematic.filtered
write.csv(problematic.full, "problematic.rows.full.csv")
write.csv(problematic.filtered, "problematic.rows.filtered.csv")

#which languages?

unique(problematic.full$FileName) %>% as.data.frame() -> problematic.doculects.full
unique(problematic.filtered$FileName) %>% as.data.frame() -> problematic.doculects.filtered
write.csv(problematic.doculects.full, "problematic.doculects.full.csv")
write.csv(problematic.doculects.filtered, "problematic.doculects.filtered.csv")

# #check mismatches between glossed and checked
# data.glossed.merged %>%
#   filter(!(FileName %in% data.glossed.checked$FileName)) -> problematic.glossed
# ###
# 
# 
#   
# data.reglossed.unfiltered %>%
#   filter(!(FileName %in% data.reglossed$FileName)) -> problematic.reglossed
# 
# all.problematic <- rbind(problematic.glossed,problematic.reglossed)
# all.problematic%>%
#   group_by(Glosser,FileName) %>%
#   summarise(n()) %>% View()
# 
# 
# all.problematic %>%
#   group_by(Glosser,Gloss)  %>%
#   summarise(n()) %>% View()
# 
# 
# all.problematic %>%
#   group_by(Glosser,NumberValue)  %>%
#   summarise(n()) %>% View()
# 
# 
# #enock's issues:
# 
# data.glossed.merged %>%
#   filter(!(ID %in% data.glossed.checked.merged$ID)) %>%
#   filter(Glosser == "EAT") -> enocks.columns
# 
# write.csv(enocks.columns, "enocks.columns.csv")

