import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Exercise } from '@/app/services/exercise'; // 👈 adapte le chemin selon où ton type est défini

type ExerciseCardProps = {
  exercise: Exercise;
  onStart: (exercise: Exercise) => void;
};

export const ExerciseCard = ({ exercise, onStart }: ExerciseCardProps) => (
  <Card className='hover:shadow-lg transition-shadow w-64 h-64'>
    <CardHeader>
      <CardTitle className='text-xl'>{exercise.name}</CardTitle>
    </CardHeader>
    <CardContent className='space-y-3'>
      <div className='grid grid-cols-2 gap-4'>
        <ExerciseDetail
          label='Inspiration'
          value={`${exercise.duration_inspiration}s`}
        />
        <ExerciseDetail
          label='Expiration'
          value={`${exercise.duration_expiration}s`}
        />
        <ExerciseDetail
          label='Apnée'
          value={`${exercise.duration_apnea}s`}
        />
        <ExerciseDetail
          label='Cycles'
          value={exercise.number_cycles.toString()}
        />
      </div>
    </CardContent>
    <CardFooter>
      <Button
        className='w-full bg-blue-600 hover:bg-blue-700'
        onClick={() => onStart(exercise)}
      >
        Commencer
      </Button>
    </CardFooter>
  </Card>
);

const ExerciseDetail = ({ label, value }: { label: string; value: string }) => (
  <div>
    <p className='text-sm text-muted-foreground'>{label}</p>
    <p className='font-medium'>{value}</p>
  </div>
);

