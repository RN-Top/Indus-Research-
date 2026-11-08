#Disclaimer: This automated coding of numeral features is based on expert input and evolved through discussions within the NumeralBank team, primarily led by Russell Barlow. While any errors in this coding are my own, the underlying concepts reflect a collective team effort

#install.packages("readr")
#install.packages("tidyverse")
library(readr)
library(tidyverse)

#create a dataframe
if (!exists("CodedNumeralBankFeatures")) {
  CodedNumeralBankFeatures <- tibble(
    Feature_ID = character(),
    Glottocode = character(),
    Source = character(),
    Value = character()
  )
}

# function to check if a "Gloss" contains an arithmetic operator and that none of the constituents is equal to the parameter in focus 
is_derived <- function(Gloss, NumberValue) {
  if (is.na(Gloss)) {
    return(NA)  # Return NA if Gloss is missing
  } else if (Gloss == "?") {
    return("?")  # Return '?' for incomplete or unclear data
  } else if (grepl("\\+|\\-|\\·", Gloss) && Gloss != as.character(NumberValue)) {
    return("1")  # Derived if it contains arithmetic operator and is not equal to NumberValue
  } else if (Gloss == as.numeric(NumberValue)) {
    return("0")  # Not derived if Gloss equals NumberValue
  } else {
    return("0")  # Default to not derived if no operator and no match to NumberValue
  }
}

# Function to process and populate based on whether the Gloss is derived
is_this_numeral_derived <- function(feature_id, NumberValue, logic_function, data) {
  # gets unique Glottocodes
  glottocodes <- unique(data$Glottocode)
  
  # a loop through each Glottocode
  for (glotto in glottocodes) {
    # Filter data for the specific NumberValue and Glottocode
    filtered_data <- data[data$NumberValue == NumberValue & data$Glottocode == glotto, ]
    
    if (nrow(filtered_data) == 0) {
      # If no data for the specific NumberValue, set value to "ID"
      CodedNumeralBankFeatures <<- rbind(CodedNumeralBankFeatures, data.frame(
        Feature_ID = feature_id,
        Glottocode = glotto,
        Source = NA,  # Set source to NA or another default value
        Value = "ID",
        stringsAsFactors = FALSE
      ))
    } else {
      # If NumberValue exists, apply the logic function to each Gloss
      for (i in 1:nrow(filtered_data)) {
        Gloss_value <- filtered_data$Gloss[i]
        value <- logic_function(Gloss_value, NumberValue)
        
        # Add a new row (preserving Source and Coder if available)
        CodedNumeralBankFeatures <<- rbind(CodedNumeralBankFeatures, data.frame(
          Feature_ID = feature_id,
          Glottocode = filtered_data$Glottocode[i],
          Source = filtered_data$Source[i],
          Value = value,
          stringsAsFactors = FALSE
        ))
      }
    }
  }
}

