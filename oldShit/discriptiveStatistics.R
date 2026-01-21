library(dplyr)
# library(nortest)

# Set working directory
setwd("/home/janno/Uni/Bingen/Semester/09_Semester/Bachelorarbeit/data/Empower-IQAir/")

# Find *_combined.csv files
files <- list.files(".", pattern = "temperature_PM_humidity\\.csv$", full.names = TRUE)

# Columns to process: named vec (new name = original CSV column)
cols_to_process <- c(
  Humidity = "Humidity....",
  Temp     = "Temperature..Celsius.",
  PM1      = "PM1..ug.m3.",
  PM25     = "PM2.5..ug.m3.",
  PM10     = "PM10..ug.m3."
)

# Function to process a single CSV
process_file <- function(file_path) {
  dataset_name <- sub("temperature_PM_humidity\\.csv", "", basename(file_path))
  message("Processing: ", dataset_name)

  data <- read.csv(file_path, stringsAsFactors = FALSE)

  # Keep only available columns and convert to numeric
  available_cols <- intersect(cols_to_process, names(data))
  data[available_cols] <- lapply(data[available_cols], function(x) as.numeric(as.character(x)))

  # Convert Celsius to Kelvin
  temp_col <- cols_to_process["Temp"]
  if (temp_col %in% available_cols) {
    data[[temp_col]] <- data[[temp_col]] + 273.15
  }

  # Descriptive statistics
  summary_vals <- data %>%
    summarise(across(all_of(available_cols),
      list(
        Min = ~ min(.x, na.rm = TRUE),
        Max = ~ max(.x, na.rm = TRUE),
        Mean = ~ mean(.x, na.rm = TRUE),
        StandardDev = ~ sd(.x, na.rm = TRUE),
        CoefficientVariation = ~ sd(.x, na.rm = TRUE) / mean(.x, na.rm = TRUE)
      ),
      .names = "{.col}_{.fn}"
    ))

  # Kolmogorov–Smirnov Tests
  ks_results <- list()

  for (orig_col in available_cols) {
    vec <- data[[orig_col]]
    vec <- vec[!is.na(vec)]
    vec <- log(vec + 1)
    # hist(vec, main = paste("Histogram of" , orig_col))
    # ad <- ad.test(vec)
    # print(ad)

    # Doesnt work, to resource intensiv
    # norm <- rnorm(length(vec), mean = mean(vec), sd = sd(vec))
    # sq <- chisq.test(vec, norm)
    # print(sq)

    if (length(vec) > 1 && sd(vec) > 0) {
      ks <- ks.test(vec, "pnorm") # , mean(vec), sd(vec)
      ks_stat <- ks$statistic
      ks_pval <- ks$p.value
      # print(ks)
    } else {
      ks_stat <- NA
      ks_pval <- NA
    }

    clean_name <- names(cols_to_process)[cols_to_process == orig_col]
    ks_results[[paste0(clean_name, "_KS_Statistic")]] <- ks_stat
    ks_results[[paste0(clean_name, "_KS_pvalue")]] <- ks_pval
  }

  ks_df <- as.data.frame(ks_results)

  # Rename descriptive columns
  new_names <- c("dataset")
  for (orig_col in available_cols) {
    clean_name <- names(cols_to_process)[cols_to_process == orig_col]
    new_names <- c(
      new_names,
      paste0(clean_name, "_Min"),
      paste0(clean_name, "_Max"),
      paste0(clean_name, "_Mean"),
      paste0(clean_name, "_sd"),
      paste0(clean_name, "_dv")
    )
  }

  colnames(summary_vals) <- new_names[-1]
  summary_vals$dataset <- dataset_name
  summary_vals <- summary_vals %>% relocate(dataset)

  # ---------- SAVE QQ-PLOTS AS PNG WITH LOG TRANSFORM FOR PM ----------
  for (orig_col in available_cols) {
    clean_name <- names(cols_to_process)[cols_to_process == orig_col]
    vec <- data[[orig_col]]
    vec <- vec[!is.na(vec)]

    # Apply log(x+1) transform ONLY to PM variables
    if (clean_name %in% c("PM1", "PM25", "PM10")) {
      vec <- log(vec + 1)
    }

    if (length(vec) > 1 && sd(vec) > 0) {
      png_filename <- paste0(dataset_name, "_", clean_name, "_QQ.png")
      png(png_filename, width = 800, height = 800)

      qqnorm(vec,
        main = paste(
          "QQ-Plot:",
          clean_name,
          "(Log-Transformed)",
          dataset_name
        )
      )
      qqline(vec, col = "red")

      dev.off()
    }
  }
  # ---------------------------------------------------------------------------

  # Combine descriptive + KS results
  final_row <- cbind(summary_vals, ks_df)
  return(final_row)
}

# Process all files
results_list <- lapply(files, process_file)
results_df <- bind_rows(results_list)

# Save final CSV
write.csv(results_df, "descriptive_statistics_with_ks.csv", row.names = FALSE)
message("Saved results to descriptive_statistics_with_ks.csv")

print(results_df)
