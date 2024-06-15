data {
    int<lower=1> N; // liczba obserwacji
    int<lower=1> D; // Liczba unikalnych kierowców
    int<lower=1> C; // Liczba unikalnych konstruktorow
    array [N] int<lower=1, upper=D> drivers; // indeksy kierowcow
    array [N] int<lower=1, upper=C> constructors; // indeksy konstruktorow
    array [N] int<lower=0, upper=19> position;
    array [N] int<lower=0, upper=1> rainy;
    array [N] int<lower=1, upper=20> qualifying_position;
}

parameters {
    array[D] real driver_skill;
    array[C] real constructor_skill;
    array[D] real driver_skill_wet;
    array[N] real overtake_coefficient;
}

transformed parameters {
    array[D] real driver_skill_sum;
    array[D] real driver_skill_qualifying;
    array[D] real driver_skill_wet_sum;
    array[N] real theta;
    for (i in 1:N) {
        driver_skill_wet_sum[drivers[i]] = (driver_skill_wet[drivers[i]]*rainy[i]);
        driver_skill_qualifying[drivers[i]] = overtake_coefficient[i] / qualifying_position[drivers[i]];
        driver_skill_sum[drivers[i]] = driver_skill[drivers[i]] + driver_skill_wet_sum[drivers[i]] + driver_skill_qualifying[drivers[i]];
        theta[i] = inv_logit(driver_skill_sum[drivers[i]] + constructor_skill[constructors[i]]);
    }
}

model {
    for (i in 1:D){
        driver_skill[i] ~ normal(0, 1);
        driver_skill_wet[i] ~ normal(0, 2);
    }
    for (i in 1:C){
        constructor_skill[i] ~ normal(0, 1);
    }
    for (i in 1:N){
        overtake_coefficient[i] ~ normal(0, 1);
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