
library(tidyverse)
library(scales)
library(latex2exp)
library(RColorBrewer)

csvs_in_dir <- "_csvs/"
plt_out_dir <- "_pdfs/"

source("utils.R")


#
# Figure 1 => imbalance ~ p_M (majority fraction) | n
#
df_fig1 <- read_csv(str_c(csvs_in_dir, "fig1_csv.csv"))

df_fig1_agg <- df_fig1 %>%
  mutate(
    delta = majority - (active_set * p_M),
    n = str_c("n = ", n),
    b_p = as.factor(b_p)
  ) %>%
  group_by(b_p, n, p_M) %>%
  summarise(
    delta_m = mean(delta),
    delta_ci = gaussian_mean_95_ci(delta),
    n_nets = n()
  )

pal_greens <- colorRampPalette(brewer.pal(n=9, "Greens"))
col_greens <- pal_greens(5)[3:5]
col_greens_transparant <- hex_with_alpha(col_greens, alpha = 0.2)

plt_fig1 <- df_fig1_agg %>%
  ggplot(aes(x=p_M, y=delta_m, color=b_p, fill=b_p)) + 
  geom_ribbon(aes(ymin=delta_m - delta_ci, ymax = delta_m + delta_ci), color=NA) +
  # geom_ribbon(aes(ymin=delta_m - delta_ci, ymax = delta_m + delta_ci), color=NA, alpha=0.2) +
  geom_line() + 
  geom_point(size = 3) +
  geom_hline(yintercept = 0, linetype = "dashed") +  
  facet_grid(. ~ n) + 
  scale_y_continuous(limits = c(-13, 13), breaks = pretty_breaks(3)) + 
  scale_color_manual(values=col_greens) +
  # scale_fill_manual(values=col_greens) +
  scale_fill_manual(values=col_greens_transparant) +
  labs(
    x = TeX("Majority fraction, $\\p_M$"),
    y = TeX("$\\Delta(S)$"),
    color = TeX("$\\b_p$")
  ) +
  guides(
    color = guide_legend(reverse = T),
    fill = "none"
  ) +  
  theme_bw() + 
  theme(
    axis.title.y = element_text(margin = margin(0, -1, 0, 0, unit = "mm")),
    strip.background = element_blank(),
    strip.text.x = element_text(size = 10, margin = margin(0, 0, 1, 0, unit = "mm")),
    panel.grid.minor = element_blank(),
    plot.margin = grid::unit(c(0, 0, 0, 0), "mm")
  )

print(plt_fig1)

ggsave(str_c(plt_out_dir, "fig1.pdf"), plot = plt_fig1, width = 5, height = 1.8)


#
# Figure 2 => assortativity ~ h (network homophily index)
#
df_fig2 <- read_csv(str_c(csvs_in_dir, "fig2_csv.csv"))

df_fig2_agg <- df_fig2 %>%
  mutate(p_M = as.factor(p_a)) %>%
  group_by(p_M, h) %>%
  summarise(
    assortativity_mean = mean(assortativity),
    n_nets = n()
  )

all(df_fig2_agg$n_nets == 20) == T

levels(df_fig2_agg$p_M) <- c(
  "0.5" = TeX("$p_M = 0.5$"),
  "0.6" = TeX("$p_M = 0.6$"),
  "0.7" = TeX("$p_M = 0.7$"),
  "0.8" = TeX("$p_M = 0.8$")
)

plt_fig2 <- df_fig2_agg %>%
  ggplot(aes(x=h, y=assortativity_mean)) + 
  geom_point(size = 2.5) +
  facet_grid(. ~ p_M, labeller = label_parsed) +
  scale_x_continuous(limits = c(0.48, 1.02)) +
  scale_y_continuous(limits = c(-0.02, 0.44), breaks = pretty_breaks()) +
  labs(
    x = TeX("Homophily index, $h$"),
    y = TeX("Assortativity index")
  ) +
  theme_bw() + 
  theme(
    axis.title.y = element_text(margin = margin(0, 0, 0, 0, unit = "mm")),
    strip.background = element_blank(),
    strip.text.x = element_text(margin = margin(1, 0, 1, 0, unit = "mm")),
    panel.grid.minor = element_blank(),
    plot.margin = grid::unit(c(-1, 1, 0, 1), "mm")
  )

print(plt_fig2)

ggsave(str_c(plt_out_dir, "fig2.pdf"), plot = plt_fig2, width = 5.5, height = 1.75)


#
# Figure 3 => imbalance ~ h (network homophily index) | p_M (majority fraction)
#
df_fig3 <- read_csv(str_c(csvs_in_dir, "fig3_csv.csv"))

df_fig3_agg <- df_fig3 %>%
  mutate(
    delta = majority - (active_set * p_M),
    p_M = as.factor(p_M),
    b_p = as.factor(b_p)
  ) %>%
  group_by(h, b_p, p_M) %>%
  summarise(
    delta_m = mean(delta),
    delta_ci = gaussian_mean_95_ci(delta),
    n_nets = n()
  )

levels(df_fig3_agg$p_M) <- c(
  "0.5" = TeX("$p_M = 0.5$"),
  "0.6" = TeX("$p_M = 0.6$"),
  "0.7" = TeX("$p_M = 0.7$"),
  "0.8" = TeX("$p_M = 0.8$")
)

pal_greens <- colorRampPalette(brewer.pal(n=9, "Greens"))
col_greens <- pal_greens(5)[3:5]
col_greens_transparant <- hex_with_alpha(col_greens, alpha = 0.2)

plt_fig3 <- df_fig3_agg %>%
  ggplot(aes(x=h, y=delta_m, color=b_p, fill=b_p)) + 
  # geom_ribbon(aes(ymin=delta_m - delta_ci, ymax = delta_m + delta_ci), color=NA, alpha=0.2) +
  geom_ribbon(aes(ymin=delta_m - delta_ci, ymax = delta_m + delta_ci), color=NA) +
  geom_line() + 
  geom_point(size = 2.8) +
  geom_hline(yintercept = 0, linetype = "dashed") +  
  facet_grid(. ~ p_M, labeller = label_parsed) + 
  scale_y_continuous(breaks = pretty_breaks()) +
  scale_color_manual(values=col_greens) +
  # scale_fill_manual(values=col_greens) +
  scale_fill_manual(values=col_greens_transparant) +
  labs(
    x = TeX("Homophily index, $h$"),
    y = TeX("$\\Delta(S)$"),
    color = TeX("$\\b_p$")
  ) +
  guides(
    color = guide_legend(keyheight = 5.2, default.unit = "mm", reverse = T),
    fill = "none"
  ) +
  theme_bw() + 
  theme(
    axis.title.x = element_text(size = 13),
    axis.title.y = element_text(size = 13, margin = margin(0, -1, 0, 0, unit = "mm")),
    axis.text = element_text(size = 9.2), 
    strip.background = element_blank(),
    strip.text.x = element_text(size = 13, margin = margin(1, 0, 1, 0, unit = "mm")),
    legend.text = element_text(size = 10),
    legend.title = element_text(size = 10, margin = margin(0, 0, -2, 0, unit = "mm")),
    legend.position = c(0.057, 0.704),
    legend.margin = margin(2, 2, 2, 7),
    panel.grid.minor = element_blank(),
    plot.margin = grid::unit(c(-1, 1, -1, 1), "mm")
  )

print(plt_fig3)

ggsave(str_c(plt_out_dir, "fig3.pdf"), plot = plt_fig3, width = 7, height = 2.1)


#
# Figure 4 => imbalance ~ h (network homophily index) | p_M (majority fraction)
#
df_fig4 <- read_csv(str_c(csvs_in_dir, "fig4_csv.csv"))

# sanity checks
unique(df_fig4$n) == 20000
unique(df_fig4$p_M) == 0.8


df_fig4_agg <- df_fig4 %>%
  mutate(
    delta = majority - (active_set * p_M),
    h_p = as.factor(h_p),
    b_p = as.factor(b_p)
  ) %>%
  group_by(b_p, h, h_p) %>%
  summarise(
    delta_m = mean(delta),
    delta_ci = gaussian_mean_95_ci(delta),
    n_nets = n()
  )

levels(df_fig4_agg$b_p) <- c(
  "0.01" = TeX("$b_p = 0.01$"),
  "0.05" = TeX("$b_p = 0.05$"),
  "0.1" = TeX("$b_p = 0.1$")
)

pal_blues <- colorRampPalette(brewer.pal(n=9, "Blues"))
col_blues <- pal_blues(9)[4:9]
col_blues_transparant <- hex_with_alpha(col_blues, alpha = 0.2)

plt_fig4 <- df_fig4_agg %>%
  ggplot(aes(x=h, y=delta_m, color=h_p, fill=h_p)) + 
  # geom_ribbon(aes(ymin=delta_m - delta_ci, ymax = delta_m + delta_ci), color=NA, alpha=0.2) +
  geom_ribbon(aes(ymin=delta_m - delta_ci, ymax = delta_m + delta_ci), color=NA) +
  geom_line() + 
  geom_point(size = 2.5) +
  geom_hline(yintercept = 0, linetype = "dashed") +  
  facet_grid(. ~ b_p, labeller = label_parsed) + 
  scale_y_continuous(breaks = pretty_breaks()) +
  scale_color_manual(values = col_blues) +
  # scale_fill_manual(values = col_blues) +
  scale_fill_manual(values = col_blues_transparant) +
  labs(
    x = TeX("Homophily index, $h$"),
    y = TeX("$\\Delta(S)$"),
    color = TeX("$\\h_p$")
  ) +
  guides(
    color = guide_legend(keyheight = 4.5, default.unit = "mm", nrow = 3, reverse = T),
    fill = "none"
  ) +
  theme_bw() + 
  theme(
    axis.title.y = element_text(margin = margin(0, -1, 0, 0, unit = "mm")),
    strip.background = element_blank(),
    strip.text.x = element_text(size=10, margin = margin(1, 0, 0.6, 0, unit = "mm")),
    legend.text = element_text(size = 9),
    legend.title = element_text(size = 9.5, margin = margin(0, 0, -2, 0, unit = "mm")),
    legend.position = c(0.118, 0.791),
    legend.margin = margin(3, 3, 3, 7),
    panel.grid.minor = element_blank(),
    plot.margin = grid::unit(c(-1, 0.5, -0.5, 0.5), "mm")
  )

print(plt_fig4)

ggsave(str_c(plt_out_dir, "fig4.pdf"), plot = plt_fig4, width = 5.5, height = 2.5)

# END