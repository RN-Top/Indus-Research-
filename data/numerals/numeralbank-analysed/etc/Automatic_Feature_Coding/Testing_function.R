#functions 
source("is_x_derived_function.R")
# test with a glossed numerals of a single language
glossed_akan_data <- read.tsv("numerals-akan1250-1.tsv")

# create a glottocode column
glossed_akan_data$Glottocode <- sub("^[^-]+-([^-]+-[0-9]+)-.*", "\\1", glossed_akan_data$ID)

#run the function: NB02	Is there a 3 derived by arithmetic operation?
is_this_numeral_derived ("NB02", 3, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB04", 4, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB06", 5, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB08", 6, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB10", 7, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB12", 8, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB14", 9, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB16", 10, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB18", 11, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB20", 12, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB22", 15, is_derived, glossed_akan_data)

is_this_numeral_derived ("NB24", 20, is_derived, glossed_akan_data)



# future self: updating the feature_ID to allow testing whether and if any number value is derived ... e.g.,
is_this_numeral_derived ("is_three_derived?", 3, is_derived, glossed_akan_data)

is_this_numeral_derived ("is_four_derived?", 4, is_derived, glossed_akan_data)

is_this_numeral_derived ("is_five_derived?", 5, is_derived, glossed_akan_data)

is_this_numeral_derived ("is_six_derived?", 6, is_derived, glossed_akan_data)


# vew resulting CodedNumeralBankFeatures dataframe
print(CodedNumeralBankFeatures)

# save results to a CSV file
write.csv(CodedNumeralBankFeatures, "CodedNumeralBankFeatures.csv", row.names = FALSE)


# test with glossed numerals of multiple languages 

glossed_15_languages <- read.tsv("glossed_15_languages.tsv")


is_this_numeral_derived ("NB02", 3, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB04", 4, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB06", 5, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB08", 6, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB10", 7, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB12", 8, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB14", 9, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB16", 10, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB18", 11, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB20", 12, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB22", 15, is_derived, glossed_15_languages)
is_this_numeral_derived ("NB24", 20, is_derived, glossed_15_languages)



# vew resulting CodedNumeralBankFeatures dataframe
print(CodedNumeralBankFeatures)

# save results to a CSV file
write.csv(CodedNumeralBankFeatures, "CodedNumeralBankFeatures.csv", row.names = FALSE)
