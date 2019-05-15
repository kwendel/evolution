
package geneticalgorithm;

import java.util.ArrayList;
import java.util.Arrays;

/**
 *
 * @author Marco Virgolin, with the collaboration of Anton Bouter and Hoang Ngoc Luong and the supervision of Peter A.N. Bosman
 */
enum CrossoverType {
    Uniform,
    OnePoint
}

public class Variation {

    CrossoverType crossover_type;

    public Variation(CrossoverType crossover_type) {
        this.crossover_type = crossover_type;
    }

    public ArrayList<Individual> PerformCrossover(Individual parent1, Individual parent2) {

        if (crossover_type == CrossoverType.OnePoint) {
            return OnePointCrossover(parent1, parent2);
        } else {
            return UniformCrossover(parent1, parent2);
        }

    }

    private ArrayList<Individual> UniformCrossover(Individual parent1, Individual parent2) {

        Individual child1 = parent1.Clone(); // explicit call to clone because otherwise Java copies the reference
        Individual child2 = parent2.Clone();
        
        // TODO: This crossover is not doing anything. You must implement it.
        // Remember to use the rng in Utilities to sample random numbers, e.g., Utilities.rng.nextDouble();

        // Assumption: childs have equal genotype length
        for (int i = 0; i < child1.genotype.length; i++) {

            // With a random chance
            if (Utilities.rng.nextDouble() > 0.5){
                // Swap the bits at this position
                int temp = child1.genotype[i];
                child1.genotype[i] = child2.genotype[i];
                child2.genotype[i] = temp;
            }
        }

        ArrayList<Individual> result = new ArrayList<Individual>();
        result.add(child1);
        result.add(child2);

        return result;
    }

    private ArrayList<Individual> OnePointCrossover(Individual parent1, Individual parent2) {

        Individual child1 = parent1.Clone();
        Individual child2 = parent2.Clone();

        // TODO: This crossover is not doing anything. You must implement it.
        // Remember to use the rng in Utilities to sample random numbers, e.g., Utilities.rng.nextDouble();

        // Assumption: childs have equal genotype length
        // Pick random point in the genotype
        int point = Utilities.rng.nextInt(child1.genotype.length);
        // Copy the parts from the crossover point
        int[] part1 = Arrays.copyOfRange(child1.genotype, point, child1.genotype.length - 1);
        int[] part2 = Arrays.copyOfRange(child2.genotype, point, child2.genotype.length - 1);
        // Place the parts in the genotypes of the childes
        System.arraycopy(part2, 0, child1.genotype, point, part2.length );
        System.arraycopy(part1, 0, child2.genotype, point, part1.length );

        ArrayList<Individual> result = new ArrayList<Individual>();
        result.add(child1);
        result.add(child2);

        return result;
    }

}
