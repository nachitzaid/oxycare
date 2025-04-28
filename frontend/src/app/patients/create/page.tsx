'use client';
import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { apiService } from '@/lib/api';
import Link from 'next/link';
import Navigation from '@/components/common/Navigation';

export default function CreatePatientPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    date_naissance: '',
    sexe: 'Homme',
    adresse: '',
    ville: '',
    code_postal: '',
    telephone: '',
    email: '',
    numero_securite_sociale: '',
    allergies: '',
    antecedents: '',
    medecin_traitant: '',
    medecin_telephone: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Rediriger si non authentifié
  if (!isAuthenticated) {
    router.push('/login');
    return null;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      await apiService.post('/patients', formData);
      router.push('/patients');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors de la création du patient');
      console.error('Erreur:', err);
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />
      
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Nouveau patient</h1>
          <Link
            href="/patients"
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Retour
          </Link>
        </div>
      </header>

      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                {error && (
                  <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                    {error}
                  </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-8 divide-y divide-gray-200">
                  <div className="space-y-8 divide-y divide-gray-200">
                    <div>
                      <h3 className="text-lg leading-6 font-medium text-gray-900">Informations personnelles</h3>
                      <div className="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                        <div className="sm:col-span-3">
                          <label htmlFor="nom" className="block text-sm font-medium text-gray-700">
                            Nom
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              name="nom"
                              id="nom"
                              required
                              value={formData.nom}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-3">
                          <label htmlFor="prenom" className="block text-sm font-medium text-gray-700">
                            Prénom
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              name="prenom"
                              id="prenom"
                              required
                              value={formData.prenom}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-3">
                          <label htmlFor="date_naissance" className="block text-sm font-medium text-gray-700">
                            Date de naissance
                          </label>
                          <div className="mt-1">
                            <input
                              type="date"
                              name="date_naissance"
                              id="date_naissance"
                              required
                              value={formData.date_naissance}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-3">
                          <label htmlFor="sexe" className="block text-sm font-medium text-gray-700">
                            Sexe
                          </label>
                          <div className="mt-1">
                            <select
                              id="sexe"
                              name="sexe"
                              value={formData.sexe}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            >
                              <option value="Homme">Homme</option>
                              <option value="Femme">Femme</option>
                            </select>
                          </div>
                        </div>

                        <div className="sm:col-span-6">
                          <label htmlFor="adresse" className="block text-sm font-medium text-gray-700">
                            Adresse
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              name="adresse"
                              id="adresse"
                              required
                              value={formData.adresse}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-2">
                          <label htmlFor="ville" className="block text-sm font-medium text-gray-700">
                            Ville
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              name="ville"
                              id="ville"
                              required
                              value={formData.ville}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-2">
                          <label htmlFor="code_postal" className="block text-sm font-medium text-gray-700">
                            Code postal
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              name="code_postal"
                              id="code_postal"
                              required
                              value={formData.code_postal}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-2">
                          <label htmlFor="telephone" className="block text-sm font-medium text-gray-700">
                            Téléphone
                          </label>
                          <div className="mt-1">
                            <input
                              type="tel"
                              name="telephone"
                              id="telephone"
                              required
                              value={formData.telephone}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-3">
                          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                            Email
                          </label>
                          <div className="mt-1">
                            <input
                              type="email"
                              name="email"
                              id="email"
                              value={formData.email}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-3">
                          <label htmlFor="numero_securite_sociale" className="block text-sm font-medium text-gray-700">
                            Numéro de sécurité sociale
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              name="numero_securite_sociale"
                              id="numero_securite_sociale"
                              value={formData.numero_securite_sociale}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="pt-8">
                      <h3 className="text-lg leading-6 font-medium text-gray-900">Informations médicales</h3>
                      <div className="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                        <div className="sm:col-span-3">
                          <label htmlFor="allergies" className="block text-sm font-medium text-gray-700">
                            Allergies
                          </label>
                          <div className="mt-1">
                            <textarea
                              id="allergies"
                              name="allergies"
                              rows={3}
                              value={formData.allergies}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-3">
                          <label htmlFor="antecedents" className="block text-sm font-medium text-gray-700">
                            Antécédents médicaux
                          </label>
                          <div className="mt-1">
                            <textarea
                              id="antecedents"
                              name="antecedents"
                              rows={3}
                              value={formData.antecedents}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="pt-8">
                      <h3 className="text-lg leading-6 font-medium text-gray-900">Médecin traitant</h3>
                      <div className="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                        <div className="sm:col-span-3">
                          <label htmlFor="medecin_traitant" className="block text-sm font-medium text-gray-700">
                            Nom du médecin
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              name="medecin_traitant"
                              id="medecin_traitant"
                              value={formData.medecin_traitant}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>

                        <div className="sm:col-span-3">
                          <label htmlFor="medecin_telephone" className="block text-sm font-medium text-gray-700">
                            Téléphone du médecin
                          </label>
                          <div className="mt-1">
                            <input
                              type="tel"
                              name="medecin_telephone"
                              id="medecin_telephone"
                              value={formData.medecin_telephone}
                              onChange={handleChange}
                              className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="pt-5">
                    <div className="flex justify-end">
                      <Link
                        href="/patients"
                        className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        Annuler
                      </Link>
                      <button
                        type="submit"
                        disabled={submitting}
                        className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        {submitting ? 'Enregistrement...' : 'Enregistrer'}
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}