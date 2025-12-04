export interface Apostle {
  id: number;
  firstName: string;
  middleName?: string;
  lastName: string;
  fullName: string;
  age: number;
  birthDate: string;
  ordinationDate: string;
  yearsInQuorum: number;
  seniority: number;
  probability?: number;
  probabilityPercent?: number;
}

export interface ApostlesData {
  metadata: {
    generatedAt: string;
    totalApostles: number;
    simulationRuns: number;
    description: string;
  };
  apostles: Apostle[];
}
