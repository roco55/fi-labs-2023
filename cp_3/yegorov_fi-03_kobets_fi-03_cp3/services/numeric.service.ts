import { mod } from "../util/mod";

export class NumericService {
  extendedGCD(a: number, b: number): number[] {
    if (a < b) {
      const temp = b;
      b = a;
      a = temp;
    }

    if (b == 0) {
      return [a, 1, 0];
    } else {
      const [gcd, x1, y1] = this.extendedGCD(b, mod(a, b));
      const x = y1;
      const y = x1 - Math.floor(a / b) * y1;

      return [gcd, x, y];
    }
  }

  getInverseModulo(a: number, n: number){
    const [gcd, _, inverseModulo] = this.extendedGCD(a, n);

    return gcd === 1 ? inverseModulo : null;
  }

  solveModuloComparison(a: number, b: number, n: number) {
    const [gcd, _, inverseModule] = this.extendedGCD(a, n);

    if (gcd === 1) {
      return mod((inverseModule * b), n);
    }

    if (b % gcd !== 0) {
      return null;
    }

    a = a / gcd;
    b = b / gcd;
    n = n / gcd;

    const x_0 = mod((this.getInverseModulo(a, n)! * b), n);

    return Array.from({ length: gcd }, (_, i) => x_0 + i * n);
  }
}
