package geneticalgorithm;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;

/**
 *
 * @author Marco Virgolin, with the collaboration of Anton Bouter and Hoang Ngoc Luong and the supervision of Peter A.N. Bosman
 */
public class Launcher {

    public static void main(String[] args) throws IOException {

        // termination condition parameters ( 0 or negatives are ignored )
        long time_limit = 3 * 1000; // in milliseconds
        int generations_limit = -1;
        long evaluations_limit = -1;

        File directory = new File("experiments");
        if (!directory.exists()) {
            directory.mkdir();
        }

        // TODO: this runs one experiment, you may want to script a pipeline here.
        int population_size = 100;
        int m = 8; int k = 5; int d = 1;
        CrossoverType ct = CrossoverType.Uniform;
        int i = 0;
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
        }
        Utilities.logger.close();

    }
}
