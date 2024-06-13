data {
    int<lower=1> D; // Liczba unikalnych kierowców
}

generated quantities {
    array[D] real driver_skill;
    array[D] real constructor_skill;
    array[D] real theta;
    array[D] int<lower=0, upper=19> position;

    for (i in 1:D) {
        driver_skill[i] = normal_rng(0, 1);
        constructor_skill[i] = normal_rng(0, 1);
        theta[i] = inv_logit(driver_skill[i] + constructor_skill[i]);
        position[i] = binomial_rng(19, theta[i]);
    }
}
