
data {
    int N;
    array [N] int<lower=1> qualifying_positions;
    array [N] real driver_skills;
    array [N] real car_skills;
}

generated quantities {
    array [N] real lambda;
    array [N] int<lower=1, upper=20> race_position;
    real alpha = normal_rng(0.1, 0.1);
    real beta = normal_rng(0.1, 0.1);
    real<lower=1, upper=20> quali = normal_rng(10, 5);
    //real alpha = normal_rng(1.6, 0.8);
    //real beta = normal_rng(1.6, 0.8);
    real<lower=0, upper=1> theta = normal_rng(0.5, 0.5);

    for (n in 1:N) {
        lambda[n] = qualifying_positions[n] + alpha * driver_skills[n] + beta * car_skills[n];
        // lambda[n] = qualifying_positions[n];
        lambda[n] = quali + alpha * driver_skills[n] + beta * car_skills[n];
        // race_position[n] = poisson_rng(lambda[n]);
        // race_position[n] = binomial_rng(N, theta);
    }
}
