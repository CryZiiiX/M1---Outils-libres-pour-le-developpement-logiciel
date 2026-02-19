/** URL de base de l'API. VITE_API_URL en build, localhost:8000 par défaut. */
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Effectue une requête HTTP vers l'API et retourne le JSON parsé.
 *
 * @param {string} path - Chemin de l'endpoint (ex: /predict, /predictions).
 * @param {RequestInit} [options={}] - Options fetch (method, body, etc.).
 * @returns {Promise<Object>} Réponse JSON.
 * @throws {Error} Si res.ok est false, avec message body.detail ou "Erreur {status}".
 */
async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Erreur ${res.status}`)
  }
  return res.json()
}

/**
 * Envoie une requête de prédiction à l'API.
 *
 * @param {Object} data - Payload : person_age, person_income, person_home_ownership,
 *   person_emp_length, loan_intent, loan_grade, loan_amnt, loan_int_rate,
 *   loan_percent_income, cb_person_default_on_file, cb_person_cred_hist_length,
 *   model_choice (optionnel, lr|dt|both).
 * @returns {Promise<Object>} Réponse : { id, created_at, model_used, lr, dt }.
 */
export function postPredict(data) {
  return request('/predict', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * Récupère l'historique des prédictions.
 *
 * @param {number} [limit=50] - Nombre max de résultats (1-200).
 * @returns {Promise<Array<Object>>} Liste des prédictions.
 */
export function getPredictions(limit = 50) {
  return request(`/predictions?limit=${limit}`)
}

/**
 * Récupère le détail d'une prédiction par son ID.
 *
 * @param {number} id - Identifiant de la prédiction.
 * @returns {Promise<Object>} Objet prédiction complet.
 */
export function getPrediction(id) {
  return request(`/predictions/${id}`)
}
