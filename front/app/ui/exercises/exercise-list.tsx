'use client';

import { Exercise } from '@/app/services/exercise';
import { ExerciseCard } from '@/app/ui/exercises/cards';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Card } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';

type ExerciseListProps = {
  exercises: ReadonlyArray<Exercise>;
  onStart: (exercise: Exercise) => void;
  loading: boolean;
};

const ExerciseList: React.FC<ExerciseListProps> = ({ exercises, onStart, loading }) => {
  if (exercises.length === 0 && loading === false) {
    return (
      <Alert>
        <AlertCircle className='h-4 w-4' />
        <AlertTitle>Pas d'exercices disponibles</AlertTitle>
        <AlertDescription>
          Pas d'exercices disponibles. Veuillez réessayer plus tard.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className='grid gap-6 md:grid-cols-2 lg:grid-cols-3'>
      {loading
        ? [1, 2, 3].map((i) => (
            <Card
              key={i}
              className='w-64 h-64'
            ></Card>
          ))
        : exercises.map((exercise) => (
            <ExerciseCard
              key={exercise.id}
              exercise={exercise}
              onStart={onStart}
            />
          ))}
    </div>
  );
};

export default ExerciseList;
