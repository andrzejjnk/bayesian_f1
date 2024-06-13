data {
    int<lower=1> N; // liczba obserwacji
    int<lower=1> D; // Liczba unikalnych kierowców
    int<lower=1> C; // Liczba unikalnych konstruktorow
    array [N] int<lower=1, upper=D> drivers; // indeksy kierowcow
    array [N] int<lower=1, upper=C> constructors; // indeksy konstruktorow
    array [N] int<lower=0, upper=19> position;
}

parameters {
    array[D] real driver_skill;
    array[C] real constructor_skill;
}

transformed parameters {
    array[N] real theta;
    for (i in 1:N) {
        theta[i] = inv_logit(driver_skill[drivers[i]] + constructor_skill[constructors[i]]);
    }
}

model {
    for (i in 1:D){
        driver_skill[i] ~ normal(2, 1);
    }
    for (i in 1:C){
        constructor_skill[i] ~ normal(2, 1);
    }
    position ~ binomial(19 , theta);
}

generated quantities {
    array [N] int<lower=0, upper=19> position_predicted;
    vector [N] log_lik;

    for (i in 1:N) {
        log_lik[i] = binomial_lpmf(position[i] | 19, theta[i]);
        position_predicted[i] = binomial_rng(19, theta[i]);
    }
}
