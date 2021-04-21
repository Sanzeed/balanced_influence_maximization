
library(tidyverse)
library(scales)
library(latex2exp)
library(RColorBrewer)
library(cowplot)
library(ggrepel)

csvs_in_dir <- "_csvs/"
plt_out_dir <- "_pdfs/"

source("utils.R")


#
# Figure 5 => Balanced influence maximization on synthetic data
#

df <- read_csv(str_c(csvs_in_dir, "fig5_csv.csv"))

# calculate delta
df <- df %>%
  mutate(
    pM = 0.8,
    delta = majority - (active_set * pM)
  )

df <- df %>%
  mutate(h_h_p = str_c("h:", h, ", h_p:", h_p))

df_agg <- df %>%
  group_by(h_h_p, h_p, lambda, gamma) %>%
  summarise(
    n_runs = n(),
    active_set_m = mean(active_set),
    active_set_ci = gaussian_mean_95_ci(active_set),
    delta_m = mean(delta),
    delta_ci = gaussian_mean_95_ci(delta)
  )
  

# tex labels
df_agg$lambda_label <- as.factor(df_agg$lambda)
levels(df_agg$lambda_label) <- c(
  "0" = TeX("$\\lambda = 0$"),
  "0.2" = TeX("$\\lambda = 0.2$"),
  "0.5" = TeX("$\\lambda = 0.5$"),
  "0.8" = TeX("$\\lambda = 0.8$"),
  "1" = TeX("$\\lambda = 1$")
)

h_h_p_labels <- unname(TeX(c(
  "$h = 0.5,  h_p = 0.5$",
  "$h = 0.5,  h_p = 0.8$",
  "$h = 0.8,  h_p = 0.8$"
)))


plt_fig5 <- df_agg %>%
  filter(h_h_p %in% c("h:0.5, h_p:0.5", "h:0.5, h_p:0.8", "h:0.8, h_p:0.8")) %>%
  ggplot(aes(x = active_set_m, y = delta_m, shape = h_h_p, color = gamma)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_errorbarh(aes(
    xmin = active_set_m - active_set_ci,
    xmax = active_set_m + active_set_ci
  ), color = "grey") +
  geom_errorbar(aes(
    ymin = delta_m - delta_ci,
    ymax = delta_m + delta_ci
  ), color = "grey") +  
  geom_path(color = "grey") + 
  geom_point(size = 3) +  
  facet_grid(. ~ lambda_label, labeller = label_parsed) + 
  scale_x_continuous(breaks = pretty_breaks()) +
  scale_y_continuous(breaks = pretty_breaks()) +
  scale_shape_discrete(labels = h_h_p_labels) +
  scale_color_gradient(low = "#56B1F7", high = "#132B43", breaks = c(0.1, 0.5, 0.9)) + 
  guides(
    shape = guide_legend(order = 1),
    color = guide_colorbar(direction = "horizontal", title.position = "top")
  ) +  
  labs(
    x = TeX("Active set size, $f(S)$"),
    y = TeX("$\\Delta(S)$"),
    color = TeX("$\\gamma$"),
    shape = "Homophily"
  ) +
  theme_bw() +
  theme(
    strip.text.x = element_text(size = 11),
    strip.text.y = element_text(size = 11),
    strip.background = element_blank()
  )

print(plt_fig5)

ggsave(str_c(plt_out_dir, "fig5.pdf"), width = 12, height = 2.75)

# END