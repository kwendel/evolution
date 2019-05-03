
package geneticalgorithm;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.util.Random;

/**
 *
 * @author Marco Virgolin, with the collaboration of Anton Bouter and Hoang Ngoc Luong and the supervision of Peter A.N. Bosman
 */
public class Utilities {
    
    // ALWAYS use this to generate random numbers, do NOT change the random seed
    public static Random rng = new Random(42424242);
    
    public static BufferedWriter logger;

    public static int [] CreateRandomPermutation(int n) {
        int [] result = new int[n];
        for(int i = 0; i < n; i++)
            result[i] = i;
        
        for (int i=0; i<n; i++) {
            int randomPosition = rng.nextInt(n);
            int temp = result[i];
            result[i] = result[randomPosition];
            result[randomPosition] = temp;
        }
        
        return result;
    }
    
}
