data {
    int N;
    array[N] int<lower=1> qualifying_positions;
    array[N] real driver_skills;
    array[N] real car_skills;
}

generated quantities {
    array[N] real<upper=20> lambda;
    array[N] int race_position;
    real alpha = normal_rng(0, 0.1);
    real beta = normal_rng(0, 0.1);
    for (n in 1:N) {
        lambda[n] = qualifying_positions[n] + alpha * driver_skills[n] + beta * car_skills[n];
        race_position[n] = binomial_rng(20, lambda[n] / 20); // 20 to górna granica
    }
}
