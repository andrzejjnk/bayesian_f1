data {
    int N; // Number od unique drivers
    real Wd; // Weight of Wins/Podiums finishes
    array [N] real Pd; // Average points per race
    real Qd; // Weight of qualifying performance
    array [N] real Ad; // Average qualifying position
    real Cd; // Weight of consistency
    array [N] real Sd; // Standard deviation of race finishes
    real sigma;
    real Pc; // Weight of performace (Race Wins, Podiums)
    // array [N] real Ec; // Engine performace (Based on reliability and power)
    real Rc; // Weight of reliability (finish  rates)
    //array [N] real Cc; // Car competitiveness (General speed and innovations)
    
}

generated quantities {
    array [N] real Rd; // Driver skill rating
    array [N] real Ccd; // Constructor skill rating
    array [N] real theta;
    array [N] int position;
    

    for (i in 1:N) {
        // Rd[i] = (Wd*Pd[i]*0.04 + Qd*(2 - (Ad[i])/10) + Cd*(2 - (Sd[i])/5)) / 3;
        Rd[i] = (normal_rng(Wd*Pd[i]*0.04, sigma) + normal_rng(Qd*(2 - (Ad[i])/10), sigma) + normal_rng(Cd*(2 - (Sd[i])/5), sigma)) / 3;
        // Ccd[i] = (Pc * Ec[i]*2 + Rc * normal_rng(0, sigma)*2) / 2;
        Ccd[i] = (Pc * normal_rng(0, sigma)*2 + Rc * normal_rng(0, sigma)*2) / 2;
        theta[i] = inv_logit(Rd[i] + Ccd[i]);
        real rd_rng = normal_rng(Rd[i], sigma);
        real ccd_rng = normal_rng(Ccd[i], sigma);
        // theta[i] = inv_logit(rd_rng + ccd_rng);
        position[i] = binomial_rng(19, theta[i]);
    }
}
