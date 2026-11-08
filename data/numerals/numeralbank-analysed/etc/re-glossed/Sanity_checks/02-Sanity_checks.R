#load libraries----
library(tidyverse)
options(tidyverse.quiet = TRUE)

#set working directory and load data----
#setwd(getSrcDirectory()[1]) # run this line if using plain R
setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) #run this line if using RStudio
setwd('..')

#Visualize NumValue as non-scientific notation
options(scipen = 1000000000)


all.data <- read.csv("all.data.csv",row.names = 1)
rownames(all.data) <- 1:nrow(all.data)

all.data %>%
  mutate(Gloss = ifelse(Gloss == "1.00E+06", 1000000,
                        ifelse(Gloss == "1.00E+05", 100000, 
                               Gloss))) %>%
  mutate(Alternate_gloss = ifelse(Alternate_gloss == "1.00E+06", 1000000,
                        ifelse(Alternate_gloss == "1.00E+05", 100000, 
                               Alternate_gloss))) -> all.data

#visualize GLOSSING----

#let's make an orthographic profile

all.data %>%
  dplyr::select(Gloss) %>%
  separate(Gloss,into=letters[1:40]) -> all.characters

all.characters %>%
  unlist() %>% 
  as.data.frame() -> all.characters.column

-sort(-table(all.characters.column$.)) %>%
  as.data.frame() -> orthography.words.profile
colnames(orthography.words.profile)[1] <- "Symbol"
write.csv(orthography.words.profile,"orthography.profile.csv")

all.data %>%
  mutate(splitGloss = strsplit(Gloss,split="")) %>% 
  dplyr::select(splitGloss) %>%
  unlist() %>%
  as.data.frame() ->all.characters.symbol

colnames(all.characters.symbol) <- "Symbol"

-sort(-table(all.characters.symbol)) %>%
  as.data.frame() -> characters.profile

write.csv(characters.profile,"characters.profile.csv")

#remove numbers and letters from the latter
characters.profile %>%
  filter(!(Symbol %in% 0:9)) %>%
  filter(!(Symbol %in% letters))  %>%
  filter(!(Symbol %in% LETTERS)) %>%
  mutate(Symbol = as.character(Symbol))-> operators.profile

#add ascii code (for some reason, this doesn't work with tidyverse)
# 
# operators.profile %>%
#   mutate(ASCII = utf8ToInt(Symbol)) %>% View()

operators.profile$ASCII <- 0

for(i in 1:nrow(operators.profile)){
  operators.profile$ASCII[i] = utf8ToInt(operators.profile$Symbol[i])
}

operators.profile %>%
  relocate(ASCII, .after = Symbol) -> operators.profile

str(operators.profile)
#-----
operators.profile.raw <- operators.profile

write.csv(operators.profile.raw,"operators.profile.raw.csv")


#Sanity checks----

#01 Empty glosses

all.data %>%
  filter(is.na(Gloss) | Gloss == "") -> no.gloss

table(no.gloss$Glosser)

write.csv(no.gloss,"errors/no.gloss.csv")

all.data %>%
  filter(Gloss != "") -> all.data

#02 Kill spaces
all.data %>%
  mutate(Gloss = str_remove_all(Gloss," ")) -> all.data

all.data %>%
  mutate(Gloss = str_replace_all(Gloss, intToUtf8(160), "")) -> all.data



#03 ? without comment
all.data %>%
  filter(Gloss == "?" & (is.na(Comment_glosser) | Comment_glosser == "") ) -> no.comment

table(no.comment$Glosser)

write.csv(no.comment,"errors/no.comment.csv")
all.data %>%
  filter(!(Gloss == "?" & (is.na(Comment_glosser) | Comment_glosser == "") ) ) -> all.data

#04 merge different symbols for the same operator



all.data %>%
  mutate(Gloss = str_replace_all(Gloss,"·", "⋅"),
         # Gloss = str_replace_all(Gloss,"\\.", "⋅"), NOT! THERE IS 12.5 IN MESOAMERICAN LANGUAGES
         Gloss = str_replace_all(Gloss,"∙", "⋅"),
         Gloss = gsub("-([]0-9½()[{}])", "−\\1", Gloss),
         Gloss = str_replace_all(Gloss,"’", "′"),
         Gloss = str_replace_all(Gloss,"\\'\\'\\'\\'", "⁗"),
         Gloss = str_replace_all(Gloss,"\\'\\'\\'", "‴"),
         Gloss = str_replace_all(Gloss,"\\'\\'", "″"),
         Gloss = str_replace_all(Gloss,"\\'", "′"),
         Gloss = str_replace_all(Gloss,"”′", "‴"),
         Gloss = str_replace_all(Gloss,"\"\"", "⁗"),
         Gloss = str_replace_all(Gloss,"”\"", "⁗"),
         Gloss = str_replace_all(Gloss,"”", "″"),
         Gloss = str_replace_all(Gloss,"′", "′"),
         Gloss = str_replace_all(Gloss,"\"", "″")
)  -> all.data


#/ is only used between letters, e.g. ({finger/arm}5⋅1)+{+?}1, so OK

#05 Matching brackets

all.data %>%
  mutate(rb = str_count(Gloss,"\\(") == str_count(Gloss,"\\)"), #matching round brackets
         sb = str_count(Gloss,"\\[") == str_count(Gloss,"\\]"), #matching square brackets
         cb = str_count(Gloss,"\\{") == str_count(Gloss,"\\}") #matching curly brackets
          ) %>%  
  filter(rb*sb*cb == 0) -> non.matching.brackets

table(non.matching.brackets$Glosser)

write.csv(non.matching.brackets,"errors/non.matching.brackets.csv")

#for the time being, we kill the problematic rows:

all.data %>%
  filter(!(ID %in% non.matching.brackets$ID) ) -> all.data

#06 Ignore text between {curly brackets} -> Gloss.clean and remove [square brackets] and ′primes′ -> Gloss.math

all.data %>%
  mutate(Gloss.clean = gsub("\\{.*?\\}","",Gloss)) %>%  #.*? NON GREEDY
  mutate(Gloss.math = gsub("\\[","",Gloss.clean),
         Gloss.math = gsub("\\]","",Gloss.math)) %>% 
  mutate(Gloss.math = gsub("′","",Gloss.math),
         Gloss.math = gsub("″","",Gloss.math),
         Gloss.math = gsub("‴","",Gloss.math),
         Gloss.math = gsub("⁗","",Gloss.math)) -> all.data


#06 find non-kosher symbols

#recalculate operators.profile----


all.data %>%
  dplyr::select(Gloss.clean) %>%
  separate(Gloss.clean,into=letters[1:45]) -> all.characters


all.characters %>%
  unlist() %>% 
  as.data.frame() -> all.characters.column

-sort(-table(all.characters.column$.)) %>%
  as.data.frame() -> orthography.words.profile
colnames(orthography.words.profile)[1] <- "Symbol"

all.data %>%
  mutate(splitGloss.clean = strsplit(Gloss.clean,split="")) %>% 
  dplyr::select(splitGloss.clean) %>%
  unlist() %>%
  as.data.frame() ->all.characters.symbol

colnames(all.characters.symbol) <- "Symbol"

-sort(-table(all.characters.symbol)) %>%
  as.data.frame() -> characters.profile


#remove numbers and letters from the latter
characters.profile %>%
  filter(!(Symbol %in% 0:9)) %>%
  # filter(!(Symbol %in% letters))  %>%
  # filter(!(Symbol %in% LETTERS)) %>%
  mutate(Symbol = as.character(Symbol))-> operators.profile

#add ascii code (for some reason, this doesn't work with tidyverse)
# 
# operators.profile %>%
#   mutate(ASCII = utf8ToInt(Symbol)) %>% View()

operators.profile$ASCII <- 0

for(i in 1:nrow(operators.profile)){
  operators.profile$ASCII[i] = utf8ToInt(operators.profile$Symbol[i])
}

operators.profile %>%
  relocate(ASCII, .after = Symbol) -> operators.profile

str(operators.profile)

write.csv(operators.profile,"operators.profile.csv")
#-----

allowed.symbols <- c("½", "⅓", "⅔", "¼", "¾", 
                     "+", "⋅", "−", "÷", 
                     "(", ")", "[", "]", "{", "}", 
                     "′", "″", "‴", "⁗", "?",".")





operators.profile %>%
  filter(!(Symbol %in% allowed.symbols)) %>%
  dplyr::select(Symbol)->  non.allowed.symbols

non.allowed.symbols %>% 
  unlist() %>%
  paste0(collapse = "") -> this

paste0("[",this,"]", collapse="") -> that

forbidden.characters <- NULL
ifelse(that == "[]", 0==0 , 
       forbidden.characters <-  all.data[(grepl(that,all.data$Gloss.clean)),])

table(forbidden.characters$Glosser)

if(that != "[]"){write_csv(forbidden.characters,"errors/forbidden.characters.csv")}

all.data %>%
  filter(!(ID %in% forbidden.characters$ID)) -> all.data

#07 Does the math add up?

#07A convert the Gloss.math column to a readable mathematical string 

all.data %>%
  mutate(Gloss.calc = gsub("⋅","\\*",Gloss.math),
         Gloss.calc = gsub("−","-",Gloss.calc),
         Gloss.calc = gsub("1½","(3/2)",Gloss.calc),         
         Gloss.calc = gsub("2½","(5/2)",Gloss.calc),    
         Gloss.calc = gsub("½","(1/2)",Gloss.calc),         
         Gloss.calc = gsub("⅓","(1/3)",Gloss.calc), 
         Gloss.calc = gsub("⅔","(2/3)",Gloss.calc),         
         Gloss.calc = gsub("¼","(1/4)",Gloss.calc),         
         Gloss.calc = gsub( "¾","(3/4)",Gloss.calc),
         Gloss.calc = gsub( "\\?",NA,Gloss.calc)) -> all.data



#fix subtraction: usually, forms such as 9 = 10-1 are noted as 9 = 1-10, hence we need some absolute value.
# Same works for cases like 19 = 10 + (1 - 10) rather than 19 = 10 + (10-1). 
#We first add the () in the cases they are missing. It should be in any subtraction, BUT not if there is a multiplication right after or right before

all.data %>%
  mutate(Gloss.calc = gsub("([0-9\\.]+)\\*([0-9\\.]+)", "\\(\\1\\*\\2\\)", Gloss.calc), #multiplication first
         Gloss.calc = gsub("([0-9\\.]+)\\/([0-9\\.]+)", "\\(\\1\\/\\2\\)", Gloss.calc), #division second 
         Gloss.calc = gsub("([0-9\\.]+)-([0-9\\.]+)", "\\(\\1-\\2\\)", Gloss.calc)) -> all.data #subtraction last

#and then we add the absolute value

all.data %>%
  mutate(Gloss.calc = gsub("\\(","abs\\(",Gloss.calc)) -> all.data

#07B Check that it's a mathematical expression

all.data %>%
  mutate(Math.well.defined =  ifelse(is.na(Gloss.calc) , NA, 
                              sapply(gsub("(\\d)\\(","\\1*(",Gloss.calc),
                                     function(x) tryCatch({ eval(parse(text = x)) 
                                                              1},
                                                          error = function(e) 0)
                              )  )) -> this

this %>%
  filter(Math.well.defined == 0 ) -> math.not.well.defined

table(math.not.well.defined$Glosser)

write.csv(math.not.well.defined,"errors/math.not.well.defined.csv")

#07C Check the math proper

this %>% 
  filter(Gloss.calc == "") -> no.math

write.csv(no.math,"errors/no.math.csv")


this %>%
  filter(Math.well.defined == 1) %>%
  filter(Gloss.calc != "") %>%
  mutate(Math.check = sapply(gsub("(\\d)\\(","\\1*(",Gloss.calc),function(x) eval(parse(text = x))),
         Math.check = unlist(Math.check),
         Math.check = abs(Math.check)) -> that
# this %>%
#   filter(Math.well.defined == 1) %>%
#   mutate(Math.check = sapply(gsub("(\\d)\\(","\\1*(",Gloss.calc),function(x) eval(parse(text = x)))) -> that
# 

that$Math.check %>%
  lengths() %>%
  as.data.frame()-> tmp
# 
# that[67528,]
# tocompare[67528,]$Gloss.calc -> Gloss.try
# that[65910,]$Gloss

that %>%
  mutate(Does.math.work = Math.check == NumberValue) -> all.data.checked


table(all.data.checked$Does.math.work,
      all.data.checked$Glosser) 

all.data.checked %>%
  filter(Does.math.work == FALSE) -> bad.math

table(bad.math$Glosser)


write.csv(bad.math, "errors/bad.math.csv")

all.data.checked %>%
  filter(Does.math.work == TRUE) -> all.data.checked

write.csv(all.data.checked,"all.data.checked.csv")
write.csv(all.data, "all.data.glossed.csv")




#summary----

table(all.data$Glosser) %>% as.data.frame()-> characters.glossed


all.data %>%
  count(Language_ID,Gloss,Glosser) %>%
  group_by(Glosser) %>%
  mutate(Glosses = n()) %>%
  ungroup() %>%
  count(Language_ID,Glosser,Glosses) %>%
  group_by(Glosser) %>%
  mutate(Languages = n()) %>%
  dplyr::select(Glosser,Languages,Glosses) %>%
  distinct() %>%
  arrange(desc(Languages)) %>%
  mutate(G.per.L = Glosses/Languages)-> stats
  
write.csv(stats,"stats.glosses.csv")


#remove typos-----

#Double ++ and trailing initial +:

all.data.checked %>%
  mutate(Gloss.math = gsub("\\+\\+","\\+",Gloss.math),
         Gloss.math = str_remove(Gloss.math,"^(\\+)"))  -> all.data.checked




#remove the 1. and .1


#this ignores the cases with two occurrences, e.g. ⋅1 and ⋅10 in the same line
all.data.checked %>%
  mutate(Gloss.math.with.ones = Gloss.math) %>%
  mutate(Gloss.math = ifelse(grepl("⋅1\\d+",Gloss.math),Gloss.math,gsub("⋅1","",Gloss.math))) %>%
  mutate(Gloss.math = ifelse(grepl("\\d+1⋅",Gloss.math),Gloss.math,gsub("1⋅","",Gloss.math))) -> all.data.checked


#this should work, but I have to fix it
all.data.checked %>%
  mutate(Gloss.math.with.ones = Gloss.math) %>%
  mutate(Gloss.math = gsub("⋅1(!\\d+)","\\1",Gloss.math)) %>%
  mutate(Gloss.math = gsub("(!\\d+)1⋅","\\1",Gloss.math)) %>%
  mutate(Gloss.math = str_remove(Gloss.math,"^(1⋅)")) %>%
  mutate(Gloss.math = str_remove(Gloss.math,"(⋅1)$")) ->all.data.checked
  
  # all.data.checked


# remove double parentheses

all.data.checked %>%
  mutate(Gloss.math = gsub("\\(\\(([0-9]+)\\)\\)","\\1",Gloss.math)) %>% #((n))
  mutate(Gloss.math = gsub("\\(\\(([0-9]+)\\+([0-9]+)\\)\\)","\\+\\1\\+\\2",Gloss.math))  %>% #((n+m))
  mutate(Gloss.math = gsub("\\(\\(([0-9]+)−([0-9]+)\\)\\)","\\(\\1\\−\\2\\)",Gloss.math)) %>% #((n−m))
  mutate(Gloss.math = gsub("\\(\\(([0-9]+)⋅([0-9]+)\\)\\)","\\1⋅\\2\\",Gloss.math)) %>% #((n⋅m))
  as.data.frame() -> all.data.checked


#remove unneccessary parentheses

all.data.checked %>%
  mutate(Gloss.math = gsub("\\(([0-9]+)\\)","\\1",Gloss.math)) %>% #(n)
  mutate(Gloss.math = gsub("\\+\\(([0-9]+)\\+([0-9]+)\\)","\\+\\1\\+\\2",Gloss.math))  %>% #+(n+m)
  mutate(Gloss.math = gsub("\\(([0-9]+)\\+([0-9]+)\\)\\+","\\1\\+\\2\\+",Gloss.math)) %>% #(n+m)+
  mutate(Gloss.math = gsub("\\(([0-9]+)⋅([0-9]+)\\)","\\1⋅\\2",Gloss.math)) %>% #(n⋅m)
  mutate(Gloss.math = gsub("^\\(([0-9]+)−([0-9]+)\\)$","\\1−\\2",Gloss.math)) %>% #^(n−m)$
  mutate(Gloss.math = gsub("^\\(([0-9]+)+([0-9]+)\\)$","\\1+\\2",Gloss.math)) %>% #^(n+m)$
  as.data.frame() -> all.data.checked

# #remove further unneccessary parentheses ((2+1)⋅6)+1 ; (5⋅2⋅2)+2 ; (10+5+5)

all.data.checked %>%
  mutate(Gloss.math = gsub("\\(([0-9]+)\\+([0-9]+)\\+([0-9]+)\\)","\\1\\+\\2\\+\\3",Gloss.math)) %>% #(n+m+q)
  mutate(Gloss.math = gsub("\\(([0-9]+)⋅([0-9]+)⋅([0-9]+)\\)","\\1⋅\\2⋅\\3",Gloss.math)) %>% #(n⋅m⋅q)
  mutate(Gloss.math = gsub("\\(\\(([0-9]+)\\+([0-9]+)\\)⋅([0-9]+)\\)","\\(\\1\\+\\2\\)⋅\\3",Gloss.math)) %>% #((n+m)⋅q)
  mutate(Gloss.math = gsub("\\(([0-9]+)⋅\\(([0-9]+)\\+([0-9]+)\\)\\)","\\1⋅\\(\\2\\+3\\)",Gloss.math)) %>% #(q⋅(n+m))
  mutate(Gloss.math = gsub("\\(\\(([0-9]+)−([0-9]+)\\)⋅([0-9]+)\\)","\\(\\1−\\2\\)⋅\\3",Gloss.math)) %>% #((n−m)⋅q)
  mutate(Gloss.math = gsub("\\(([0-9]+)⋅\\(([0-9]+)−([0-9]+)\\)\\)","\\1⋅\\(\\2−3\\)",Gloss.math)) %>% #(q⋅(n−m))
  as.data.frame() -> all.data.checked

#remove +0

all.data.checked %>%
  mutate(Gloss.math = str_remove(Gloss.math,"\\+0")) -> all.data.checked
  

  
write.csv(all.data.checked,"all.data.checked.csv")

