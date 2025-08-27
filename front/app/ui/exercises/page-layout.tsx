import React from 'react';

interface PageLayoutProps {
  children: React.ReactNode;
  showHeader?: boolean;
}

const PageLayout = ({
  children,
  showHeader = true,
}: {
  children: React.ReactNode;
  showHeader?: boolean;
}) => (
  <div className='flex flex-col items-center mx-auto h-full'>
    {showHeader && (
      <div className='flex flex-col space-y-2 mb-8'>
        <h1 className='text-3xl font-bold'>Exercices de respiration</h1>
        <p className='text-muted-foreground'>
          Choisissez un exercice pour commencer votre séance de respiration. Installez vous dans un
          endroit calme. Durée estimée de l'exercice: 5 minutes.
        </p>
      </div>
    )}
    {children}
  </div>
);

export default PageLayout;
