data {
  int<lower=1> N;                // Liczba obserwacji
  int<lower=1> K;                // Liczba kategorii
  array[N] real<lower=0, upper=2> d;    // driver_skill
  array[N] real<lower=0, upper=2> ds;   // driver skill seasonal
  array[N] real<lower=0, upper=2> t;    // car skill
  array[N] real<lower=0, upper=2> ts;   // car skill seasonal
}

parameters {
  real<lower=0> sigma_d; // Odchylenie standardowe dla driver_skill
  real<lower=0> sigma_ds; // Odchylenie standardowe dla driver skill seasonal
  real<lower=0> sigma_t; // Odchylenie standardowe dla car skill
  real<lower=0> sigma_ts; // Odchylenie standardowe dla car skill seasonal
  ordered[K-1] cutpoints;  // Punkty odcięcia dla ordered logistic
}

model {
  // Priory
  sigma_d ~ normal(0, 1);
  sigma_ds ~ normal(0, 1);
  sigma_t ~ normal(0, 1);
  sigma_ts ~ normal(0, 1);
  cutpoints ~ normal(0, 1);
}

generated quantities {
  // Wyznaczanie pozycji kierowców
  array[N] int<lower=1, upper=K> position;
  vector[N] param;
  for (i in 1:N) {
    param[i] = d[i] * sigma_d + ds[i] * sigma_ds + t[i] * sigma_t + ts[i] * sigma_ts;
    position[i] = ordered_logistic_rng(param[i], cutpoints);
  }
}








