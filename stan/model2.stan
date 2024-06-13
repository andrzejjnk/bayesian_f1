data {
    int<lower=1> D; // Liczba unikalnych kierowców
    array [D] int<lower=0, upper=1> rainy;
}

generated quantities {
    array[D] real driver_skill;
    array[D] real driver_skill_wet;
    array[D] real driver_skill_sum;
    array[D] real constructor_skill;
    array[D] real theta;
    array[D] int<lower=0, upper=19> position;

    for (i in 1:D) {
        driver_skill[i] = normal_rng(0, 1);
        driver_skill_wet[i] = normal_rng(0, 2) * rainy[i];
        driver_skill_sum[i] = driver_skill[i] + driver_skill_wet[i];
        constructor_skill[i] = normal_rng(0, 1);
        theta[i] = inv_logit(driver_skill_sum[i] + constructor_skill[i]);
        position[i] = binomial_rng(19, theta[i]);
    }
}
