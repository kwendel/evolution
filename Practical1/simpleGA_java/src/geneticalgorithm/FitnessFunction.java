
package geneticalgorithm;

/**
 *
 * @author Marco Virgolin, with the collaboration of Anton Bouter and Hoang Ngoc Luong and the supervision of Peter A.N. Bosman
 */
public class FitnessFunction {

    int m, k, d;
    long evaluations;
    double optimum;

    Individual elite = null;

    FitnessFunction(int m, int k, int d) {
        this.m = m;
        this.k = k;
        this.d = d;
        this.evaluations = 0;

        this.optimum = m * k;   // TODO: this is the optimum for OneMax, not for your function
    }
    
    // The purpose of this custom exception is to perform a naughty trick: halt the GA as soon as the optimum is found
    // do not modify it
    class OptimumFoundCustomException extends Exception {
        public OptimumFoundCustomException(String message) {
            super(message);
        }
    }

    public void Evaluate(Individual individual) throws OptimumFoundCustomException, OptimumFoundCustomException {

        evaluations++;
        
        // TODO: You have to implement the correct evaluation function. The following is OneMax (counts 1s). Remember to modify the optimum as well.
        double result = 0;

        for (int i = 0; i < individual.genotype.length; i++) {
            result += individual.genotype[i];
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
