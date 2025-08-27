'use client';

import { useState, useEffect, useRef } from 'react';
import { getExercises, Exercise, ExercisesResponse } from '@/app/services/exercise';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertCircle, Play, Pause, X } from 'lucide-react';
import { HiCheckCircle } from 'react-icons/hi';
import PageLayout from '@/app/ui/exercises/page-layout';

enum BreathingPhase {
  INSPIRATION = 'inspiration',
  EXPIRATION = 'expiration',
  APNEA = 'apnea',
}

const PHASE_CONFIG = {
  [BreathingPhase.INSPIRATION]: {
    label: 'Inspiration',
    color: 'blue',
    instruction: 'Inspirez',
    durationKey: 'duration_inspiration',
  },
  [BreathingPhase.EXPIRATION]: {
    label: 'Expiration',
    color: 'green',
    instruction: 'Expirez',
    durationKey: 'duration_expiration',
  },
  [BreathingPhase.APNEA]: {
    label: 'Apnée',
    color: 'purple',
    instruction: 'Bloquez votre respiration',
    durationKey: 'duration_apnea',
  },
} as const;

type ExerciseCardProps = {
  exercise: Exercise;
  onStart: (exercise: Exercise) => void;
};

const ExerciseCard = ({ exercise, onStart }: ExerciseCardProps) => (
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

const LoadingSkeleton = () => (
  <div className='grid gap-6 md:grid-cols-2 lg:grid-cols-3'>
    {[1, 2, 3].map((i) => (
      <Card
        key={i}
        className='w-full'
      >
        <CardHeader>
          <Skeleton className='h-6 w-3/4' />
        </CardHeader>
        <CardContent className='space-y-4'>
          {[1, 2, 3, 4].map((j) => (
            <div
              key={j}
              className='flex justify-between items-center'
            >
              <Skeleton className='h-4 w-1/2' />
              <Skeleton className='h-4 w-1/4' />
            </div>
          ))}
        </CardContent>
        <CardFooter>
          <Skeleton className='h-10 w-full rounded-md' />
        </CardFooter>
      </Card>
    ))}
  </div>
);

export default function BreathingPage() {
  const [exercises, setExercises] = useState<ExercisesResponse>({ exercises: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [currentPhase, setCurrentPhase] = useState<BreathingPhase>(BreathingPhase.INSPIRATION);
  const [timeLeft, setTimeLeft] = useState(0);
  const [currentCycle, setCurrentCycle] = useState(1);
  const [isStarting, setIsStarting] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  const [countdown, setCountdown] = useState(3);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const countdownRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    console.log('[STATE DEBUG]', {
      exercises,
      loading,
      error,
      currentExercise,
      isRunning,
      currentPhase,
      timeLeft,
      currentCycle,
      isStarting,
      isFinished,
      countdown,
      timerRef: timerRef.current,
      countdownRef: countdownRef.current,
    });
  }, [
    exercises,
    loading,
    error,
    currentExercise,
    isRunning,
    currentPhase,
    timeLeft,
    currentCycle,
    isStarting,
    isFinished,
    countdown,
    timerRef,
    countdownRef,
  ]);

  useEffect(() => {
    fetchExercises();
  }, []);

  const fetchExercises = async () => {
    try {
      const data = await getExercises();
      setExercises(data);
    } catch (err) {
      console.error('Error loading exercises:', err);
      setError('Impossible de charger les exercices. Veuillez réessayer plus tard.');
    } finally {
      setLoading(false);
    }
  };

  const buildDictColor = (color: string) => {
    return {
      fill: `bg-${color}-200`,
      bg: `bg-${color}-50`,
      text: `text-${color}-800`,
      border: `border-${color}-200`,
    };
  };

  const getPhaseColor = () => {
    return buildDictColor(PHASE_CONFIG[currentPhase].color);
  };

  const startExercise = (exercise: Exercise) => {
    setCurrentExercise(exercise);
    setIsStarting(true);
    setCountdown(3);

    countdownRef.current = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(countdownRef.current!);
          setIsStarting(false);
          setCurrentPhase(BreathingPhase.INSPIRATION);
          setTimeLeft(exercise.duration_inspiration);
          setCurrentCycle(1);
          setIsRunning(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const resetExercise = (finished = false) => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    if (countdownRef.current) {
      clearInterval(countdownRef.current);
      countdownRef.current = null;
    }

    if (finished) {
      setIsFinished(true);
    } else {
      setIsFinished(false);
    }
    setCurrentExercise(null);
    setIsRunning(false);
    setIsStarting(false);
  };

  const togglePause = () => {
    setIsRunning(!isRunning);
  };

  const handleNextPhase = () => {
    if (!currentExercise) {
      console.error('Aucun exercice lancé');
      return 0;
    }
    if (currentPhase === BreathingPhase.INSPIRATION) {
      if (currentExercise?.[PHASE_CONFIG[BreathingPhase.APNEA]?.durationKey] !== 0) {
        setCurrentPhase(BreathingPhase.APNEA);
        return currentExercise.duration_apnea;
      } else {
        setCurrentPhase(BreathingPhase.EXPIRATION);
        return currentExercise.duration_expiration;
      }
    }

    if (currentPhase === BreathingPhase.APNEA) {
      setCurrentPhase(BreathingPhase.EXPIRATION);
      return currentExercise.duration_expiration;
    }

    const isLastCycle = currentCycle >= currentExercise.number_cycles;
    if (isLastCycle) {
      clearInterval(timerRef.current!);
      resetExercise(true);
      return 0;
    }

    setCurrentCycle(currentCycle + 1);
    setCurrentPhase(BreathingPhase.INSPIRATION);
    return currentExercise.duration_inspiration;
  };

  useEffect(() => {
    if (!isRunning || !currentExercise) return;
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          return handleNextPhase();
        }
        return prev - 1;
      });
    }, 1000);
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isRunning, currentPhase, currentCycle, currentExercise]);

  const getFillHeight = () => {
    if (![BreathingPhase.INSPIRATION, BreathingPhase.EXPIRATION].includes(currentPhase)) {
      return '100%';
    }
    const duration = currentExercise?.[PHASE_CONFIG[currentPhase]?.durationKey];
    if (!duration) return '0%';
    const percentage = ((duration - timeLeft + 1) / duration) * 100;
    return currentPhase === BreathingPhase.EXPIRATION ? `${100 - percentage}%` : `${percentage}%`;
  };

  // --------------------------
  // Finished screen
  // --------------------------
  if (isFinished) {
    return (
      <PageLayout showHeader={false}>
        <div className='flex flex-col items-center justify-center space-y-8 py-12 text-center'>
          <div className='w-32 h-32 bg-green-100 rounded-full flex items-center justify-center'>
            <HiCheckCircle className='w-20 h-20 text-green-600' />
          </div>
          <h2 className='text-3xl font-bold'>Exercice terminé !</h2>
          <p className='text-xl text-muted-foreground'>
            Félicitations, vous avez terminé votre séance de respiration.
          </p>
          <Button
            onClick={() => {
              resetExercise();
            }}
            className='mt-4'
            size='lg'
          >
            Retour aux exercices
          </Button>
        </div>
      </PageLayout>
    );
  }

  // --------------------------
  // Exercise screen
  // --------------------------
  if (currentExercise) {
    return (
      <PageLayout showHeader={false}>
        <div className='flex flex-col items-center justify-center space-y-8 py-12'>
          {isStarting ? (
            <>
              <div className='text-center space-y-2'>
                <h2 className='text-2xl font-bold'>{currentExercise.name}</h2>
                <p className='text-muted-foreground'>Préparation de l'exercice</p>
              </div>
              <div className='rounded-full w-64 h-64 flex items-center justify-center text-8xl font-bold bg-gray-100 text-gray-800'>
                {countdown}
              </div>
              <p className='text-xl font-medium'>Début dans...</p>
            </>
          ) : (
            <>
              <div className='text-center space-y-2'>
                <h2 className='text-2xl font-bold'>{currentExercise.name}</h2>
                <p className='text-muted-foreground'>
                  Cycle {currentCycle} sur {currentExercise.number_cycles}
                </p>
              </div>

              <div className='relative w-64 h-64'>
                <div className='absolute inset-0 rounded-full border-4 border-gray-200 overflow-hidden'>
                  <div className='absolute inset-0 bg-gray-50'></div>
                  <div
                    className={`absolute bottom-0 left-0 right-0 transition-all duration-1000 ease-linear ${getPhaseColor().fill}`}
                    style={{ height: getFillHeight() }}
                  ></div>
                  <div className='absolute inset-0 flex items-center justify-center'>
                    <div
                      className={`w-56 h-56 rounded-full flex items-center justify-center text-5xl font-bold z-10 ${getPhaseColor().bg} ${getPhaseColor().text}`}
                    >
                      {timeLeft}s
                    </div>
                  </div>
                </div>
              </div>

              <p className='text-xl font-medium'>{PHASE_CONFIG[currentPhase].instruction}</p>

              <div className='flex space-x-4'>
                <Button
                  variant='outline'
                  size='lg'
                  className='gap-2'
                  onClick={togglePause}
                >
                  {isRunning ? <Pause className='h-5 w-5' /> : <Play className='h-5 w-5' />}
                  {isRunning ? 'Pause' : 'Reprendre'}
                </Button>
                <Button
                  variant='outline'
                  size='lg'
                  className='gap-2'
                  onClick={() => resetExercise()}
                >
                  <X className='h-5 w-5' />
                  Arrêter
                </Button>
              </div>
            </>
          )}
        </div>
      </PageLayout>
    );
  }

  // --------------------------
  // Loading
  // --------------------------
  if (loading) {
    return (
      <PageLayout>
        <LoadingSkeleton />
      </PageLayout>
    );
  }

  if (error) {
    return (
      <PageLayout>
        <Alert variant='destructive'>
          <AlertCircle className='h-4 w-4' />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </PageLayout>
    );
  }

  if (exercises.exercises.length === 0) {
    return (
      <PageLayout>
        <Alert>
          <AlertCircle className='h-4 w-4' />
          <AlertTitle>Pas d'exercices disponibles</AlertTitle>
          <AlertDescription>
            Pas d'exercices disponibles. Veuillez réessayer plus tard.
          </AlertDescription>
        </Alert>
      </PageLayout>
    );
  }

  // --------------------------
  // Exercise list
  // --------------------------
  return (
    <PageLayout>
      <div className='grid gap-6 md:grid-cols-2 lg:grid-cols-3'>
        {exercises.exercises.map((exercise) => (
          <ExerciseCard
            key={exercise.id}
            exercise={exercise}
            onStart={startExercise}
          />
        ))}
      </div>
    </PageLayout>
  );
}
