data {
    int<lower=1> N; // liczba obserwacji
    int<lower=1> D; // Liczba unikalnych kierowców
    int<lower=1> C; // Liczba unikalnych konstruktorow
    array [N] int<lower=1, upper=D> drivers; // indeksy kierowcow
    array [N] int<lower=1, upper=C> constructors; // indeksy konstruktorow
    array [N] int<lower=0, upper=19> position;
    array [N] int<lower=0, upper=1> rainy;
}

parameters {
    array[D] real driver_skill;
    array[C] real constructor_skill;
    array[D] real driver_skill_wet;
    array[C] real constructor_skill_track_temp;
}

transformed parameters {
    array[D] real driver_skill_sum;
    array[C] real constructor_skill_sum;
    array[C] real constructor_skill_sum_track_temp;
    array[N] real theta;
    for (i in 1:N) {
        driver_skill_sum[drivers[i]] = driver_skill[drivers[i]] + driver_skill_wet[drivers[i]]*rainy[i];
        constructor_skill_sum_track_temp[constructors[i]]  = constructor_skill_track_temp[constructors[i]];
        constructor_skill_sum[constructors[i]] = constructor_skill[constructors[i]] + constructor_skill_sum_track_temp[constructors[i]];
        theta[i] = inv_logit(driver_skill_sum[drivers[i]] + constructor_skill_sum[constructors[i]]);
    }
}

model {
    for (i in 1:D){
        driver_skill[i] ~ normal(0, 1);
        driver_skill_wet[i] ~ normal(0, 2);
    }
    for (i in 1:C){
        constructor_skill[i] ~ normal(0, 1);
        constructor_skill_track_temp[i] ~ normal(0, 0.5);
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