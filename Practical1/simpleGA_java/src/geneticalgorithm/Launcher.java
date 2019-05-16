package geneticalgorithm;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * @author Marco Virgolin, with the collaboration of Anton Bouter and Hoang Ngoc Luong and the supervision of Peter A.N. Bosman
 */

public class Launcher {
    // termination condition parameters ( 0 or negatives are ignored )
    private static final long time_limit = 3 * 1000; // in milliseconds
    private static final int generations_limit = -1;
    private static final long evaluations_limit = -1;
    private static int runs = 100;

    private ArrayList<Experiment> dingen;

    public Launcher() {
        int[] all_ps = {2, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200};
        CalcD k_0 = k -> 0;
        CalcD k_1_k = k -> 1.0 / k;
        CalcD k_1_1_k = k -> 1.0 - 1.0 / k;
        CalcD k_1 = k -> 1;

        dingen = new ArrayList<>();

        // analyze_d
        int k = 10;
        dingen.addAll(Experiment.combinations(
                new CalcD[]{k_0, k_1_k, k_1_1_k},
                new int[]{k},
                new int[]{4},
                all_ps
        ));
        dingen.add(new Experiment(k_0, k, 4, 200));
        dingen.add(new Experiment(k_1_k, k, 4, 200));
        dingen.add(new Experiment(k_1_1_k, k, 4, 200));
        dingen.add(new Experiment(k_1, k, 4, 200));

        // analyze_popsize
        dingen.addAll(Experiment.combinations(
                new CalcD[]{k_1_k},
                new int[]{5},
                new int[]{2},
                all_ps
        ));
        dingen.addAll(Experiment.combinations(
                new CalcD[]{k_1_k},
                new int[]{10},
                new int[]{8},
                all_ps
        ));

        // analyze_popsize_big
        dingen.addAll(Experiment.combinations(
                new CalcD[]{k_1_k},
                new int[]{10},
                new int[]{8},
                Arrays.stream(all_ps).map(p -> p > 2 ? p * 10 : p).toArray() // [2, 100, 200, ..., 2000]
        ));

        // analyze_m_k
        dingen.addAll(Experiment.combinations(
                new CalcD[]{k_1_k},
                new int[]{3, 5, 10, 50},
                new int[]{1, 2, 4, 8, 16},
                new int[]{20}
        ));
//
//        // analyze_m_k_2
        dingen.add(new Experiment(k_1_k, 2, 10, 20));
        dingen.add(new Experiment(k_1_k, 10, 2, 20));
        dingen.add(new Experiment(k_1_k, 2, 30, 20));
        dingen.add(new Experiment(k_1_k, 30, 2, 20));
        dingen.add(new Experiment(k_1_k, 2, 50, 20));
        dingen.add(new Experiment(k_1_k, 50, 2, 20));
        dingen.add(new Experiment(k_1_k, 10, 15, 20));
        dingen.add(new Experiment(k_1_k, 15, 10, 20));
        dingen.add(new Experiment(k_1_k, 15, 30, 20));
        dingen.add(new Experiment(k_1_k, 30, 15, 20));
    }

    public static void main(String[] args) throws IOException {
        new Launcher().run();
    }

    private void run() throws IOException {
        File directory = new File("experiments");
        if (!directory.exists()) {
            directory.mkdir();
        }

        for (Experiment experiment : dingen) {
            runSingle(experiment, CrossoverType.OnePoint);
            runSingle(experiment, CrossoverType.Uniform);
        }
    }

    private void runSingle(Experiment experiment, CrossoverType ct) throws IOException {
        int population_size = experiment.p;
        int m = experiment.m;
        int k = experiment.k;
        double d = experiment.d;

        for (int i = 0; i < runs; i++) {
            // Set up logging
            String output_file_name = "experiments/log_p" + population_size + "_m" + m + "_k" + k + "_d" + d + "_c" + ct + "_run" + i + ".txt";
            Files.deleteIfExists(new File(output_file_name).toPath());
            Utilities.logger = new BufferedWriter(new FileWriter(output_file_name, true));
            Utilities.logger.write("gen evals time best_fitness\n");

            // Run GA
            System.out.println("Starting run " + i + " with pop_size=" + population_size + ", m=" + m + ", k=" + k + ", d=" + d + ", crossover_type=" + ct);
            SimpleGeneticAlgorithm ga = new SimpleGeneticAlgorithm(population_size, m, k, d, ct);
            try {
                ga.run(generations_limit, evaluations_limit, time_limit);

                System.out.println("Best fitness " + ga.fitness_function.elite.fitness + " found at\n"
                        + "generation\t" + ga.generation + "\nevaluations\t" + ga.fitness_function.evaluations + "\ntime (ms)\t" + (System.currentTimeMillis() - ga.start_time + "\n")
                        + "elite\t\t" + ga.fitness_function.elite.toString());

            } catch (FitnessFunction.OptimumFoundCustomException ex) {
                System.out.println("Optimum " + ga.fitness_function.elite.fitness + " found at\n"
                        + "generation\t" + ga.generation + "\nevaluations\t" + ga.fitness_function.evaluations + "\ntime (ms)\t" + (System.currentTimeMillis() - ga.start_time + "\n")
                        + "elite\t\t" + ga.fitness_function.elite.toString());
                Utilities.logger.write(ga.generation + " " + ga.fitness_function.evaluations + " " + (System.currentTimeMillis() - ga.start_time) + " " + ga.fitness_function.elite.fitness + "\n");
            } finally {
                int ones = (int) ga.fitness_function.sumGenotype(ga.fitness_function.elite.genotype);
                int zeros = ga.fitness_function.elite.genotype.length;
                zeros = zeros - ones;

                Utilities.logger.write(ga.fitness_function.elite + " " + zeros + " " + ones);
                Utilities.logger.close();
            }
        }
    }
}
