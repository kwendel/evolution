package geneticalgorithm;

import java.util.ArrayList;
import java.util.List;

class Experiment {
    int k;
    int m;
    int p;
    double d;

    public Experiment(CalcD d, int k, int m, int p) {
        this.k = k;
        this.m = m;
        this.p = p;
        this.d = d.d(k);
    }

    static List<Experiment> combinations(CalcD[] ds, int[] ks, int[] ms, int[] ns) {
        List<Experiment> dingen = new ArrayList<>(ks.length * ms.length * ns.length);
        for (CalcD d : ds) {
            for (int k : ks) {
                for (int m : ms) {
                    for (int n : ns) {
                        dingen.add(new Experiment(d, k, m, n));
                    }
                }
            }
        }
        return dingen;
    }
}


