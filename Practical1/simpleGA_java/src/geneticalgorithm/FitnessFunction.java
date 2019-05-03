
package geneticalgorithm;

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
        this.optimum = 1; // The optimal is achieved when u(b) = k and thus fitness=1
    }
    
    // The purpose of this custom exception is to perform a naughty trick: halt the GA as soon as the optimum is found
    // do not modify it
    class OptimumFoundCustomException extends Exception {
        public OptimumFoundCustomException(String message) {
            super(message);
        }
    }

    private double sumGenotype(Individual individual) {
        double result = 0;

        for (int i = 0; i < individual.genotype.length; i++) {
            result += individual.genotype[i];
        }

        return result;
    }

    private double fp1(Individual individual) {
        // Compute the sum over the genotype - u(b)
        double ub = this.sumGenotype(individual);

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
        double result = this.fp1(individual); // practical 1 fitness

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
