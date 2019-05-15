
package geneticalgorithm;

import java.util.Arrays;

/**
 *
 * @author Marco Virgolin, with the collaboration of Anton Bouter and Hoang Ngoc Luong and the supervision of Peter A.N. Bosman
 */
public class FitnessFunction {

    int m, k;
    double d;
    long evaluations;
    double optimum;

    Individual elite = null;

    FitnessFunction(int m, int k, double d) {
        this.m = m;
        this.k = k;
        this.d = d;
        this.evaluations = 0;

//        this.optimum = m * k;   // TODO: this is the optimum for OneMax, not for your function
        this.optimum = m; // The optimal is achieved when u(b) = k and thus fitness=1
    }
    
    // The purpose of this custom exception is to perform a naughty trick: halt the GA as soon as the optimum is found
    // do not modify it
    class OptimumFoundCustomException extends Exception {
        public OptimumFoundCustomException(String message) {
            super(message);
        }
    }

    public double sumGenotype(int[] genotype) {
        double result = 0;

        for (int i = 0; i < genotype.length; i++) {
            result += genotype[i];
        }

        return result;
    }

    public double fp1(int[] genoSubrange) {
        // Compute the sum over the genotype - u(b)
//        double ub = this.sumGenotype(individual);
        double ub = this.sumGenotype(genoSubrange);

        // return fitness according to the two cases
        if (ub == this.k) {
            return 1;
        } else {
            return (1 - this.d) * ((k - 1 - ub) / (k - 1));
        }
    }

    public void Evaluate(Individual individual) throws OptimumFoundCustomException {

        evaluations++;
        
        // Compute the fitness of the individual
//        double result = this.sumGenotype(individual); // OneMax -- counts 1s


        // Practical 1 fitness
        double result = 0;
        for (int i = 0; i < this.m; i++) {
            int[] subrange = Arrays.copyOfRange(individual.genotype, i * this.k, i * this.k + this.k);
            result += this.fp1(subrange);
        }

        // set the fitness of the individual
        individual.fitness = result;

        // update elite
        if (elite == null || elite.fitness < individual.fitness) {
            elite = individual.Clone();
        }

        // check if optimum has been found
        if (result == optimum) {
            // naughty trick in action: throw our custom exception
            throw new OptimumFoundCustomException("GG EZ");
        }
    }

    

}
