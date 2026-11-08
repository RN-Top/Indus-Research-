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

setwd("..")


#South Asian languages_MAIN----


setwd("./South Asian languages_MAIN")
temp.data <- NULL
temp = list.files( pattern="\\.csv$")
myfiles = lapply(temp, function(x) {
  data = read.csv(x)
  data$FileName = x
  data
})

names(myfiles) <- temp
length(myfiles)
#850 files



myfiles %>%
  lapply(ncol) %>% 
  cbind.data.frame() %>%  
  t() -> all.ncols
table(all.ncols)
# 
# all.ncols
# 14 
# 850  
all.ncols %>%
  as.data.frame() %>%
  filter(V1 > 14) 

# myfiles[[1]] %>% colnames()
# myfiles[[1]] %>% head()
# 
# #14 columns
# myfiles[["AA069-numerals-east2330-1.csv"]] %>% colnames()
# myfiles[["AA069-numerals-east2330-1.csv"]] %>% head()
# myfiles[["AA069-numerals-east2330-1.csv"]] <- myfiles[["AA069-numerals-east2330-1.csv"]][,-1]
# colnames(myfiles[["AA069-numerals-east2330-1.csv"]])[1] <- "X"
# 
# #15 columns
# myfiles[["IE104-numerals-kach1272-1.csv"]] %>% colnames()
# myfiles[["IE104-numerals-kach1272-1.csv"]] %>% head()
# myfiles[["IE104-numerals-kach1272-1.csv"]] <- myfiles[["IE104-numerals-kach1272-1.csv"]][,-c(1,2)]
# colnames(myfiles[["IE104-numerals-kach1272-1.csv"]])[1] <- "X"
# 
# myfiles[["ST061-numerals-koch1250-1.csv"]] %>% colnames()
# myfiles[["ST061-numerals-koch1250-1.csv"]] %>% head()
# myfiles[["ST061-numerals-koch1250-1.csv"]] <- myfiles[["ST061-numerals-koch1250-1.csv"]][,-c(1,2)]
# colnames(myfiles[["ST061-numerals-koch1250-1.csv"]])[1] <- "X"
# 
# #16 columns
# myfiles[["DV003-numerals-mudh1235-1.csv"]] %>% colnames()
# myfiles[["DV003-numerals-mudh1235-1.csv"]] %>% head()
# myfiles[["DV003-numerals-mudh1235-1.csv"]] <- myfiles[["DV003-numerals-mudh1235-1.csv"]][,-c(1,2,3)]
# colnames(myfiles[["DV003-numerals-mudh1235-1.csv"]])[1] <- "X"
# 
# myfiles[["ST058-numerals-deor1238-1.csv"]] %>% colnames()
# myfiles[["ST058-numerals-deor1238-1.csv"]] %>% head()
# myfiles[["ST058-numerals-deor1238-1.csv"]]  <- myfiles[["ST058-numerals-deor1238-1.csv"]][,-c(14,15,16)]


myfiles %>%
  lapply(colnames) %>% 
  cbind.data.frame() %>% 
  t() %>%
  as.data.frame()-> all.columns

for(i in 1:ncol(all.columns)){
  print(table(all.columns[,i])) }

# #which element does not contain a given col name
# names(myfiles)[!sapply(myfiles, \(df) "X" %in% names(df))]
# 
# myfiles[["DV017-numerals-irul1243-1.csv"]] %>% colnames()
# myfiles[["DV017-numerals-irul1243-1.csv"]] %>% head()
# colnames(myfiles[["DV017-numerals-irul1243-1.csv"]])[1] <- "X"
# 
# myfiles[["IE268-googleuninum-hat.csv"]] %>% colnames()
# myfiles[["IE268-googleuninum-hat.csv"]] %>% head()
# colnames(myfiles[["IE268-googleuninum-hat.csv"]])[1] <- "X"
# 
# names(myfiles)[!sapply(myfiles, \(df) "Comment_glosser" %in% names(df))]
# 
# myfiles[["IE162-numerals-urdu1245-1.csv"]] %>% colnames()
# myfiles[["IE162-numerals-urdu1245-1.csv"]] %>% head()


# colnames(myfiles[["IE162-numerals-urdu1245-1.csv"]])[c(12,13)] <- c("Comment_glosser","Alternate_gloss")


do.call(rbind.data.frame, myfiles) -> temp.data

setwd("..")
#Add glosser name
glossers <- read.csv("glossers_for_re-glossed.csv")

left_join(temp.data, glossers, join_by(FileName == File) ) -> temp.data

#temp.data$Glosser <- "KM+NK+RB"

#basic checks
colnames(temp.data)

#unique numeral ID's:
temp.data %>%
  group_by(ID) %>%
  filter(n()>1) -> duplicates.SA_Main


# write.csv(duplicates.SA_Main,"duplicates.SA_Main.csv")


##no duplicated rows!

#all Language_ID's present
-sort(-table(temp.data$Language_ID, useNA = "ifany"))
sum(is.na(temp.data$Language_ID))

#all Sources present
-sort(-table(temp.data$Source, useNA = "ifany"))

rbind(all.data,temp.data) -> all.data


#South Asian languages_alternative-doculects----


setwd("./South Asian languages_alternative-doculects")
temp.data <- NULL
temp = list.files( pattern="\\.csv$")
myfiles = lapply(temp, function(x) {
  data = read.csv(x)
  data$FileName = x
  data
})

names(myfiles) <- temp
length(myfiles)
#63 files



myfiles %>%
  lapply(ncol) %>% 
  cbind.data.frame() %>%  
  t() -> all.ncols
table(all.ncols)


myfiles %>%
  lapply(colnames) %>% 
  cbind.data.frame() %>% 
  t() %>%
  as.data.frame()-> all.columns

for(i in 1:ncol(all.columns)){
  print(table(all.columns[,i])) }


do.call(rbind.data.frame, myfiles) -> temp.data


#Add glosser name
# temp.data$Glosser <- "KM+NK+RB"

left_join(temp.data, glossers, join_by(FileName == File) ) -> temp.data

#basic checks
colnames(temp.data)

#unique numeral ID's:
temp.data %>%
  group_by(ID) %>%
  filter(n()>1)


##no duplicated rows!

#all Language_ID's present
-sort(-table(temp.data$Language_ID, useNA = "ifany"))
sum(is.na(temp.data$Language_ID))

#all Sources present
-sort(-table(temp.data$Source, useNA = "ifany"))

rbind(all.data,temp.data) -> all.data
setwd("..")

#other languages----


setwd("./other languages")
temp.data <- NULL
temp = list.files( pattern="\\.csv$")
myfiles = lapply(temp, function(x) {
  data = read.csv(x)
  data$FileName = x
  data
})

names(myfiles) <- temp
length(myfiles)
#88 files



myfiles %>%
  lapply(ncol) %>% 
  cbind.data.frame() %>%  
  t() -> all.ncols
table(all.ncols)

# 14 
# 88  
all.ncols %>%
  as.data.frame() %>%
  filter(V1 > 13) 

myfiles[[1]] %>% colnames()
myfiles[[1]] %>% head()



myfiles %>%
  lapply(colnames) %>% 
  cbind.data.frame() %>% 
  t() %>%
  as.data.frame()-> all.columns

for(i in 1:ncol(all.columns)){
  print(table(all.columns[,i])) }

do.call(rbind.data.frame, myfiles) -> temp.data

setwd("..")


#Add glosser name
# temp.data$Glosser <- "RE-GLOSSED"
left_join(temp.data, glossers, join_by(FileName == File) ) -> temp.data

#basic checks
colnames(temp.data)

#unique numeral ID's:
temp.data %>%
  group_by(ID) %>%
  filter(n()>1)



##no duplicated rows!

#all Language_ID's present
-sort(-table(temp.data$Language_ID, useNA = "ifany"))
sum(is.na(temp.data$Language_ID))

#all Sources present
-sort(-table(temp.data$Source, useNA = "ifany"))

rbind(all.data,temp.data) -> all.data




write.csv(all.data,"all.data.csv")

