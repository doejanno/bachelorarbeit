library(dplyr)
library(tidyr)
library(ggplot2)

# Set working directory
setwd("/home/janno/Uni/Bingen/Semester/09_Semester/Bachelorarbeit/data/Empower-IQAir/")

# Find *_combined.csv files
files <- list.files(".", pattern = "_combined\\.csv$", full.names = TRUE)

# Columns to process
cols_to_process <- c(
  Humidity = "Humidity....",
  Temp     = "Temperature..Celsius.",
  PM1      = "PM1..ug.m3.",
  PM25     = "PM2.5..ug.m3.",
  PM10     = "PM10..ug.m3."
)

# Load all CSVs and add dataset name
data_list <- lapply(files, function(file) {
  name <- sub("_combined\\.csv", "", basename(file))
  message("Loading: ", name)
  
  df <- read.csv(file)
  df$dataset <- name
  df
})

# Combine all datasets
all_data <- bind_rows(data_list)

# Keep only relevant columns
selected_cols <- intersect(c("dataset", cols_to_process), names(all_data))
all_data <- all_data[, selected_cols]

# Convert numeric columns
num_cols <- setdiff(names(all_data), "dataset")
all_data[num_cols] <- lapply(all_data[num_cols], function(x) as.numeric(as.character(x)))

# Pivot to long format for plotting (boxplots)
long_data <- pivot_longer(
  all_data,
  cols = -dataset,
  names_to = "variable",
  values_to = "value"
)

# Remove NA values
long_data <- long_data %>% filter(!is.na(value))

# -------------------------------
# Shift values slightly above 0 for log scale
# -------------------------------
epsilon <- 1  # small constant to avoid log(0)
long_data <- long_data %>% mutate(value_shifted = value + epsilon)

# -------------------------------
# Log-scale boxplots
# -------------------------------
p_boxlog <- ggplot(long_data, aes(x = dataset, y = value_shifted, fill = dataset)) +
  geom_boxplot(outlier.shape = 1, coef = 3) +
  facet_wrap(~ variable, scales = "free_y") +
  scale_y_log10() +
  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "none"
  ) +
  labs(
    title = "Boxplots of Humidity and PM Values (Log Scale, zeros included)",
    x = "Dataset",
    y = paste0("Value + ", epsilon, " (log scale)")
  )

print(p_boxlog)

message("Log-scale boxplots generated successfully (zeros included with small shift).")

# =====================================================================
#                     SIMPLE GRAPH (INDEX VS DATA)
# =====================================================================

# Add index column per dataset
all_data_with_index <- all_data %>%
  group_by(dataset) %>%
  mutate(index = row_number()) %>%
  ungroup()

# Pivot to long form
long_index <- pivot_longer(
  all_data_with_index,
  cols = all_of(num_cols),
  names_to = "variable",
  values_to = "value"
)

# Simple line plot
p_simple <- ggplot(long_index, aes(x = index, y = value, color = dataset)) +
  geom_line(alpha = 0.7) +
  facet_wrap(~ variable, scales = "free_y") +
  theme_bw() +
  labs(
    title = "Simple Plot of Variables Over Index",
    x = "Index",
    y = "Value"
  )

print(p_simple)

message("Simple index-based plots generated successfully.")

# ============================================================
#                     Q–Q PLOTS
# ============================================================

p_qq <- ggplot(long_data, aes(sample = value, color = dataset)) +
  stat_qq(alpha = 0.6) +
  stat_qq_line() +
  facet_wrap(~ variable, scales = "free") +
  theme_bw() +
  theme(
    legend.position = "bottom",
    axis.text.x = element_text(angle = 45, hjust = 1)
  ) +
  labs(
    title = "Q–Q Plots of Variables",
    x = "Theoretical Quantiles",
    y = "Sample Quantiles"
  )

print(p_qq)

message("Q–Q plots generated successfully.")
