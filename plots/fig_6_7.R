
library(tidyverse)
library(scales)
library(latex2exp)
library(RColorBrewer)
library(cowplot)

csvs_in_dir <- "_csvs/"
plt_out_dir <- "_pdfs/"

source("utils.R")

# fraction of majority nodes in each network
net_pM <- tribble(
  ~network, ~pM,
  "bofa_careers",    0.77,
  "upsjobs",         0.69,
  "verizoncareers",  0.77,
  "hersheycareers",  0.68
)

#
# Figure 6 => Balanced influence maximization on Twitter graphs
#
df_mu_div <- read_csv(str_c(csvs_in_dir, "fig6_csv.csv"))

# add majority fractions & compute the expected majority
df_mu_div <- df_mu_div %>% inner_join(net_pM, by="network")

# delta = observed majority - expected majority
df_mu_div <- df_mu_div %>% mutate(delta = majority - (active_set * pM))

# sanity check
unique(df_mu_div$b_p) == 0.01

# compute aggregate stats
df_mu_div <- df_mu_div %>%
  group_by(network, lambda, gamma, h_p) %>%
  summarise(
    n_runs = n(),
    active_set_m = mean(active_set),
    active_set_ci = gaussian_mean_95_ci(active_set),
    delta_m = mean(delta),
    delta_ci = gaussian_mean_95_ci(delta)    
  )


# plot
nets <- c("bofa_careers", "upsjobs", "verizoncareers", "hersheycareers")

pal_reds <- colorRampPalette(brewer.pal(n=9, "Reds"))
pal_greens <- colorRampPalette(brewer.pal(n=9, "Greens"))

col_reds <- pal_reds(13)[5:13]
col_greens <- pal_greens(13)[5:13]

df_mu_div$lambda_label <- as.factor(df_mu_div$lambda)
levels(df_mu_div$lambda_label) <- c(
    "0" = TeX("$\\lambda = 0$"),
    "0.2" = TeX("$\\lambda = 0.2$"),
    "0.5" = TeX("$\\lambda = 0.5$"),
    "0.8" = TeX("$\\lambda = 0.8$"),
    "1" = TeX("$\\lambda = 1$")
  )

plt_mu_dev_1 <- df_mu_div %>%
  filter(network == nets[1]) %>%
  ggplot(aes(x=active_set_m, y=delta_m, color=interaction(gamma, h_p), shape=as.factor(h_p))) + 
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
  geom_hline(yintercept = 0, linetype = "dashed") +
  facet_grid(network ~ lambda_label, labeller = label_parsed) + 
  scale_x_continuous(breaks = pretty_breaks()) +
  scale_colour_manual(values = c(col_reds, col_greens)) +
  labs(x=NULL, y = TeX("$\\Delta(S)$")) +
  theme_bw() +
  theme(
    legend.position = "none", 
    strip.background = element_blank(),
    strip.text.x = element_text(size = 11),
    strip.text.y = element_text(size = 11)    
  )

plt_mu_dev_2 <- df_mu_div %>%
  filter(network == nets[2]) %>%
  ggplot(aes(x=active_set_m, y=delta_m, color=interaction(gamma, h_p), shape=as.factor(h_p))) + 
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
  geom_hline(yintercept = 0, linetype = "dashed") +
  facet_grid(network ~ lambda_label, labeller = label_parsed) + 
  scale_x_continuous(breaks = pretty_breaks()) +
  scale_colour_manual(values = c(col_reds, col_greens)) +
  labs(x=NULL, y = TeX("$\\Delta(S)$")) +
  theme_bw() +
  theme(
    legend.position = "none", 
    strip.background = element_blank(), 
    strip.text.x = element_blank(),
    strip.text.y = element_text(size = 11)
  )

plt_mu_dev_3 <- df_mu_div %>%
  filter(network == nets[3]) %>%
  ggplot(aes(x=active_set_m, y=delta_m, color=interaction(gamma, h_p), shape=as.factor(h_p))) + 
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
  geom_hline(yintercept = 0, linetype = "dashed") +
  facet_grid(network ~ lambda_label, labeller = label_parsed) + 
  scale_x_continuous(breaks = pretty_breaks()) +
  scale_colour_manual(values = c(col_reds, col_greens)) +
  labs(x=NULL, y = TeX("$\\Delta(S)$")) +
  theme_bw() +
  theme(
    legend.position = "none", 
    strip.background = element_blank(), 
    strip.text.x = element_blank(),
    strip.text.y = element_text(size = 11)
  )

plt_mu_dev_4 <- df_mu_div %>%
  filter(network == nets[4]) %>%
  ggplot(aes(x=active_set_m, y=delta_m, color=interaction(gamma, h_p), shape=as.factor(h_p))) + 
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
  geom_hline(yintercept = 0, linetype = "dashed") +
  facet_grid(network ~ lambda_label, labeller = label_parsed) + 
  scale_x_continuous(breaks = pretty_breaks()) +
  scale_colour_manual(values = c(col_reds, col_greens)) +
  labs(x=TeX("Active set size, $f(S)$"), y = TeX("$\\Delta(S)$")) +
  theme_bw() +
  theme(
    legend.position = "none", 
    strip.background = element_blank(), 
    strip.text.x = element_blank(),
    strip.text.y = element_text(size = 11)
  )

legend_shape <- ggplot() + 
  geom_point(aes(x=c(1,2), y=1, shape=factor(c("0.5", "0.8"))), size=3) + 
  labs(shape = TeX("$h_p$")) + 
  theme_bw()

legend_shape <- get_legend(legend_shape)

legend_red <- ggplot() + 
  geom_point(aes(x=seq(0.1, 0.9, 0.1), y=1, col=seq(0.1, 0.9, 0.1)), size=3) + 
  scale_colour_gradient(low=col_reds[1], high = col_reds[9], breaks=c(0.1, 0.5, 0.9)) + 
  labs(color = TeX("$\\gamma$")) + 
  theme_bw()

legend_red <- get_legend(legend_red)

legend_green <- ggplot() + 
  geom_point(aes(x=seq(0.1, 0.9, 0.1), y=1, col=seq(0.1, 0.9, 0.1)), size=3) + 
  scale_colour_gradient(low=col_greens[1], high = col_greens[9], breaks=c(0.1, 0.5, 0.9)) + 
  labs(color = TeX("$\\gamma$")) + 
  theme_bw()

legend_green <- get_legend(legend_green)

plt_mu_div <- plot_grid(
  plot_grid(
    plt_mu_dev_1, 
    plt_mu_dev_2, 
    plt_mu_dev_3, 
    plt_mu_dev_4, 
    ncol = 1,
    rel_heights = c(1.0, 0.9, 0.9, 1.0)
  ),
  plot_grid(
    legend_shape,
    legend_red,
    legend_green,
    ncol = 1
  ),
  rel_widths = c(1, 0.08)
)

print(plt_mu_div)

save_plot(
  str_c(plt_out_dir, "fig6.pdf"),
  plt_mu_div,
  base_width = 12,
  base_height = 7
)


#
# Figure 7 => Baseline vs our method on Twitter graphs
#

# read and process the results of the baseline algorithm
df_base <- read_csv(str_c(csvs_in_dir, "fig7_csv.csv"))

# add majority fractions & compute the expected majority
df_base <- df_base %>% inner_join(net_pM, by="network")

# delta = observed majority - expected majority
df_base <- df_base %>% mutate(delta = majority - (active_set * pM))

# sanity check
unique(df_base$b_p) == 0.01

# aggregate
df_base <- df_base %>%
  filter(abs(offset) <= 50) %>%
  group_by(network, h_p, offset) %>%
  summarise(
    n_runs = n(),
    active_set_m = mean(active_set),
    active_set_ci = gaussian_mean_95_ci(active_set),
    delta_m = mean(delta),
    delta_ci = gaussian_mean_95_ci(delta)        
  ) %>%
  filter(abs(delta_m) < 500)  
  # NB: there are some weird cases, k_offset led to negative values
  # => Ok to ignore these

#
# Baseline vs ours
#
# Lambda = 0.5, all gammas
#

df_jp_lambda <- bind_rows(
  df_base %>%
    rename(in_param = offset) %>%
    select(-n_runs) %>%
    mutate(method = "base"),
  df_mu_div %>% 
    ungroup() %>%
    filter(lambda == 0.5) %>%
    rename(in_param = gamma) %>% 
    select(-n_runs, -lambda) %>%
    mutate(method = "mu_div")
)

pal_reds <- colorRampPalette(brewer.pal(n=9, "Reds"))
pal_blues <- colorRampPalette(brewer.pal(n=9, "Blues"))

col_reds <- pal_reds(15)[5:15]
col_blues <- pal_blues(13)[5:13]

df_jp_lambda$h_p_label <- as.factor(df_jp_lambda$h_p)
levels(df_jp_lambda$h_p_label) <- c(
    "0.5" = TeX("$h_p = 0.5$"),
    "0.8" = TeX("$h_p = 0.8$")
  )

plt_jp_lambda <- df_jp_lambda %>%
  ungroup() %>%
  mutate(
    network = fct_relevel(network, c("bofa_careers", "upsjobs", "verizoncareers", "hersheycareers"))
  ) %>%
  ggplot(aes(
    x = active_set_m,
    y = delta_m,
    color = interaction(as.factor(in_param), method),
    shape = method
  )) + 
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
  geom_hline(yintercept = 0, linetype = "dashed") +
  facet_grid(h_p_label ~ network, scales="free_x", labeller = label_parsed) +
  scale_x_continuous(breaks = pretty_breaks()) +
  scale_colour_manual(values = c(col_reds, col_blues)) +
  labs(x=TeX("Active set size, $f(S)$"), y = TeX("$\\Delta(S)$")) +
  theme_bw() +
  theme(
    legend.position = "none",
    strip.background = element_blank(),
    strip.text.x = element_text(size = 11, face = "bold"),
    strip.text.y = element_text(size = 11, face = "bold")
  )

legend_shape <- ggplot() + 
  geom_point(aes(x=c(1,2), y=1, shape=factor(c("Baseline", "Ours"))), size=3) + 
  labs(shape = "Method") + 
  theme_bw() +
  theme(legend.title=element_text(size=13))  

legend_shape <- get_legend(legend_shape)

legend_red <- ggplot() + 
  geom_point(aes(x=seq(-50, 50, 10), y=1, col=seq(-50, 50, 10)), size=3) + 
  scale_colour_gradient(low=col_reds[1], high = col_reds[11]) + 
  labs(color = TeX("$k_{offset}$")) +
  guides(color = guide_colorbar(direction = "horizontal", title.position = "top")) +
  theme_bw() + 
  theme(legend.title=element_text(size=13))  

legend_red <- get_legend(legend_red)

legend_blue <- ggplot() + 
  geom_point(aes(x=seq(0.1, 0.9, 0.1), y=1, col=seq(0.1, 0.9, 0.1)), size=3) + 
  scale_colour_gradient(low=col_blues[1], high = col_blues[9], breaks=c(0.1, 0.5, 0.9)) + 
  labs(color = TeX("$\\gamma$")) + 
  guides(color = guide_colorbar(direction = "horizontal", title.position = "top")) +
  theme_bw() + 
  theme(legend.title=element_text(size=14))
  
legend_blue <- get_legend(legend_blue)

plt_fig7 <- plot_grid(
  plt_jp_lambda, 
  plot_grid(
    legend_shape,
    legend_red,
    legend_blue,
    ncol = 1,
    align = "v",
    rel_heights = c(0.6, 0.9, 0.9)
  ), 
  rel_widths = c(1, 0.15),
  rel_heights = c(1.0, 0.8),
  nrow = 1
)

print(plt_fig7)

save_plot(
  str_c(plt_out_dir, "fig7.pdf"),
  plt_fig7,
  base_width = 12,
  base_height = 4
)

# END