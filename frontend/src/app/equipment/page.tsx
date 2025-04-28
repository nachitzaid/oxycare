// src/app/equipment/page.tsx
'use client';
import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiService } from '@/lib/api';
import Navigation from '@/components/common/Navigation';

interface Equipment {
  id: number;
  numero_serie: string;
  modele: string;
  type_equipement: string;
  fabricant: string;
  statut: string;
  date_acquisition: string;
  patient_id: number | null;
}

export default function EquipmentPage() {
  const [equipments, setEquipments] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchEquipments = async () => {
      try {
        setLoading(true);
        const data = await apiService.get('/equipments');
        setEquipments(data);
      } catch (err: any) {
        setError(err.message || 'Erreur lors du chargement des équipements');
        console.error('Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchEquipments();
  }, [isAuthenticated, router]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />

      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Équipements</h1>
          <Link 
            href="/equipment/create" 
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Nouvel équipement
          </Link>
        </div>
      </header>
      
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {error && (
            <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          
          <div className="px-4 py-6 sm:px-0">
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <ul className="divide-y divide-gray-200">
                {equipments.length > 0 ? (
                  equipments.map((equipment) => (
                    <li key={equipment.id}>
                      <Link href={`/equipment/${equipment.id}`} className="block hover:bg-gray-50">
                        <div className="px-4 py-4 sm:px-6">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <div className="ml-3">
                                <p className="text-sm font-medium text-blue-600 truncate">
                                  {equipment.modele} - {equipment.numero_serie}
                                </p>
                                <p className="text-sm text-gray-500">
                                  {equipment.type_equipement} | {equipment.fabricant}
                                </p>
                              </div>
                            </div>
                            <div className="ml-2 flex-shrink-0 flex">
                              <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                                ${equipment.statut === 'disponible' ? 'bg-green-100 text-green-800' : 
                                equipment.statut === 'en service' ? 'bg-blue-100 text-blue-800' : 
                                equipment.statut === 'en maintenance' ? 'bg-yellow-100 text-yellow-800' : 
                                'bg-red-100 text-red-800'}`}
                              >
                                {equipment.statut}
                              </p>
                            </div>
                          </div>
                          <div className="mt-2 sm:flex sm:justify-between">
                            <div className="sm:flex">
                              <p className="flex items-center text-sm text-gray-500">
                                <span>Acquisition: {new Date(equipment.date_acquisition).toLocaleDateString()}</span>
                              </p>
                              <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                                <span>Statut: {equipment.patient_id ? 'Attribué' : 'Non attribué'}</span>
                              </p>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </li>
                  ))
                ) : (
                  <li className="px-4 py-5 text-center text-gray-500">
                    Aucun équipement trouvé.
                  </li>
                )}
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}