import React from 'react';

type ExerciseCountdownProps = {
  readonly name: string;
  readonly countdown: number;
};

export default function ExerciseCountdown({ name, countdown }: ExerciseCountdownProps) {
  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold">{name}</h2>
        <p className="text-muted-foreground">Préparation de l'exercice</p>
      </div>
      <div className="rounded-full w-64 h-64 flex items-center justify-center text-8xl font-bold bg-gray-100 text-gray-800">
        {countdown}
      </div>
      <p className="text-xl font-medium">Début dans...</p>
    </div>
  );
}
