package geneticalgorithm;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;

/**
 * @author Marco Virgolin, with the collaboration of Anton Bouter and Hoang Ngoc Luong and the supervision of Peter A.N. Bosman
 */

public class Launcher {
    // termination condition parameters ( 0 or negatives are ignored )
    private static final long time_limit = 3 * 1000; // in milliseconds
    private static final int generations_limit = -1;
    private static final long evaluations_limit = -1;
    private static final int runs = 25;

    private CalcD[] ds = new CalcD[]{
//            k -> 0,
            k -> 1.0 / k,
//            k -> 1.0 - 1.0 / k,
//            k -> 1
    };
    //    private int[] ks = new int[]{3, 5, 10};
    private int[] ks = new int[]{10};
    //    private int[] ms = new int[]{1, 2, 4, 8, 16};
    private int[] ms = new int[]{8};
    //    private int[] ns = new int[]{2, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190
//            ,200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400};
    private int[] ns = new int[]{2, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000};
    //    private int[] ns = new int[]{200};
    private CrossoverType[] cts = new CrossoverType[]{CrossoverType.OnePoint, CrossoverType.Uniform};

    public static void main(String[] args) throws IOException {
        new Launcher().run();
    }

    private void run() throws IOException {
        File directory = new File("experiments_big");
        if (!directory.exists()) {
            directory.mkdir();
        }

        for (int k : ks) {
            for (int m : ms) {
                for (CalcD calcD : ds) {
                    double d = calcD.d(k);
                    for (int n : ns) {
                        for (CrossoverType ct : cts) {
                            runSingle(n, m, k, d, ct);
                        }
                    }
                }
            }
        }
//        runSingle(10, 3, 5, 1.0/3, CrossoverType.Uniform);
    }

    private void runSingle(int population_size, int m, int k, double d, CrossoverType ct) throws IOException {
        for (int i = 0; i < runs; i++) {
            // Set up logging
            String output_file_name = "experiments_big/log_p" + population_size + "_m" + m + "_k" + k + "_d" + d + "_c" + ct + "_run" + i + ".txt";
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

    interface CalcD {
        double d(int k);
    }
}
