import geography from "./geography.json"

/**
 * Thailand Geography Data Helper
 * Provides functions to work with Thailand geography data including provinces, districts, and subdistricts
 */
class ThailandGeography {
    constructor(data) {
        this.data = data;
    }

    /**
     * Get all provinces in Thailand
     * @returns {Array} Array of unique provinces with their codes and names
     */
    getAllProvinces() {
        const provinces = new Map();

        this.data.forEach(item => {
            if (!provinces.has(item.provinceCode)) {
                provinces.set(item.provinceCode, {
                    provinceCode: item.provinceCode,
                    provinceNameEn: item.provinceNameEn,
                    provinceNameTh: item.provinceNameTh
                });
            }
        });

        return Array.from(provinces.values()).sort((a, b) => a.provinceCode - b.provinceCode);
    }

    /**
     * Get all districts in a specific province
     * @param {number|string} provinceCode - The province code
     * @returns {Array} Array of unique districts in the specified province
     */
    getDistrictsByProvince(provinceCode) {
        const districts = new Map();
        const numProvinceCode = Number(provinceCode);

        this.data.forEach(item => {
            if (item.provinceCode === numProvinceCode) {
                if (!districts.has(item.districtCode)) {
                    districts.set(item.districtCode, {
                        provinceCode: item.provinceCode,
                        provinceNameEn: item.provinceNameEn,
                        provinceNameTh: item.provinceNameTh,
                        districtCode: item.districtCode,
                        districtNameEn: item.districtNameEn,
                        districtNameTh: item.districtNameTh
                    });
                }
            }
        });

        return Array.from(districts.values()).sort((a, b) => a.districtCode - b.districtCode);
    }

    /**
     * Get all subdistricts in a specific district
     * @param {number|string} provinceCode - The province code
     * @param {number|string} districtCode - The district code
     * @returns {Array} Array of subdistricts in the specified district
     */
    getSubdistrictsByDistrict(provinceCode, districtCode) {
        const numProvinceCode = Number(provinceCode);
        const numDistrictCode = Number(districtCode);

        return this.data
            .filter(item => item.provinceCode === numProvinceCode && item.districtCode === numDistrictCode)
            .map(item => ({
                provinceCode: item.provinceCode,
                provinceNameEn: item.provinceNameEn,
                provinceNameTh: item.provinceNameTh,
                districtCode: item.districtCode,
                districtNameEn: item.districtNameEn,
                districtNameTh: item.districtNameTh,
                subdistrictCode: item.subdistrictCode,
                subdistrictNameEn: item.subdistrictNameEn,
                subdistrictNameTh: item.subdistrictNameTh,
                postalCode: item.postalCode
            }))
            .sort((a, b) => a.subdistrictCode - b.subdistrictCode);
    }

    /**
     * Get all subdistricts in a specific province
     * @param {number|string} provinceCode - The province code
     * @returns {Array} Array of all subdistricts in the specified province
     */
    getSubdistrictsByProvince(provinceCode) {
        const numProvinceCode = Number(provinceCode);

        return this.data
            .filter(item => item.provinceCode === numProvinceCode)
            .map(item => ({
                provinceCode: item.provinceCode,
                provinceNameEn: item.provinceNameEn,
                provinceNameTh: item.provinceNameTh,
                districtCode: item.districtCode,
                districtNameEn: item.districtNameEn,
                districtNameTh: item.districtNameTh,
                subdistrictCode: item.subdistrictCode,
                subdistrictNameEn: item.subdistrictNameEn,
                subdistrictNameTh: item.subdistrictNameTh,
                postalCode: item.postalCode
            }))
            .sort((a, b) => a.subdistrictCode - b.subdistrictCode);
    }

    /**
     * Get postal codes for a specific subdistrict
     * @param {number|string} provinceCode - The province code
     * @param {number|string} districtCode - The district code
     * @param {number|string} subdistrictCode - The subdistrict code
     * @returns {Array} Array of postal codes for the specified subdistrict
     */
    getPostalCodes(provinceCode, districtCode, subdistrictCode) {
        const numProvinceCode = Number(provinceCode);
        const numDistrictCode = Number(districtCode);
        const numSubdistrictCode = Number(subdistrictCode);

        const postalCodes = new Set();

        this.data.forEach(item => {
            if (item.provinceCode === numProvinceCode &&
                item.districtCode === numDistrictCode &&
                item.subdistrictCode === numSubdistrictCode) {
                postalCodes.add(item.postalCode);
            }
        });

        return Array.from(postalCodes).sort();
    }

    /**
     * Search provinces by name (English or Thai)
     * @param {string} searchTerm - The search term
     * @returns {Array} Array of matching provinces
     */
    searchProvinces(searchTerm) {
        const term = searchTerm.toLowerCase();
        const provinces = this.getAllProvinces();

        return provinces.filter(province =>
            province.provinceNameEn.toLowerCase().includes(term) ||
            province.provinceNameTh.includes(searchTerm)
        );
    }

    /**
     * Search districts by name within a province
     * @param {number|string} provinceCode - The province code
     * @param {string} searchTerm - The search term
     * @returns {Array} Array of matching districts
     */
    searchDistricts(provinceCode, searchTerm) {
        const term = searchTerm.toLowerCase();
        const districts = this.getDistrictsByProvince(provinceCode);

        return districts.filter(district =>
            district.districtNameEn.toLowerCase().includes(term) ||
            district.districtNameTh.includes(searchTerm)
        );
    }

    /**
     * Search subdistricts by name within a district
     * @param {number|string} provinceCode - The province code
     * @param {number|string} districtCode - The district code
     * @param {string} searchTerm - The search term
     * @returns {Array} Array of matching subdistricts
     */
    searchSubdistricts(provinceCode, districtCode, searchTerm) {
        const term = searchTerm.toLowerCase();
        const subdistricts = this.getSubdistrictsByDistrict(provinceCode, districtCode);

        return subdistricts.filter(subdistrict =>
            subdistrict.subdistrictNameEn.toLowerCase().includes(term) ||
            subdistrict.subdistrictNameTh.includes(searchTerm)
        );
    }

    /**
     * Get complete address information by codes
     * @param {number|string} provinceCode - The province code
     * @param {number|string} districtCode - The district code (optional)
     * @param {number|string} subdistrictCode - The subdistrict code (optional)
     * @returns {Object} Complete address information
     */
    getAddressInfo(provinceCode, districtCode = null, subdistrictCode = null) {
        const numProvinceCode = Number(provinceCode);
        const numDistrictCode = districtCode ? Number(districtCode) : null;
        const numSubdistrictCode = subdistrictCode ? Number(subdistrictCode) : null;

        let filters = [item => item.provinceCode === numProvinceCode];

        if (numDistrictCode) {
            filters.push(item => item.districtCode === numDistrictCode);
        }

        if (numSubdistrictCode) {
            filters.push(item => item.subdistrictCode === numSubdistrictCode);
        }

        const result = this.data.find(item => filters.every(filter => filter(item)));

        if (result) {
            return {
                provinceCode: result.provinceCode,
                provinceNameEn: result.provinceNameEn,
                provinceNameTh: result.provinceNameTh,
                districtCode: result.districtCode,
                districtNameEn: result.districtNameEn,
                districtNameTh: result.districtNameTh,
                subdistrictCode: result.subdistrictCode,
                subdistrictNameEn: result.subdistrictNameEn,
                subdistrictNameTh: result.subdistrictNameTh,
                postalCode: result.postalCode
            };
        }

        return null;
    }

    /**
     * Find addresses by postal code
     * @param {number|string} postalCode - The postal code
     * @returns {Array} Array of addresses with the specified postal code
     */
    getAddressByPostalCode(postalCode) {
        const numPostalCode = Number(postalCode);

        return this.data
            .filter(item => item.postalCode === numPostalCode)
            .map(item => ({
                provinceCode: item.provinceCode,
                provinceNameEn: item.provinceNameEn,
                provinceNameTh: item.provinceNameTh,
                districtCode: item.districtCode,
                districtNameEn: item.districtNameEn,
                districtNameTh: item.districtNameTh,
                subdistrictCode: item.subdistrictCode,
                subdistrictNameEn: item.subdistrictNameEn,
                subdistrictNameTh: item.subdistrictNameTh,
                postalCode: item.postalCode
            }));
    }

    /**
     * Get statistics about the geography data
     * @returns {Object} Statistics object containing counts
     */
    getStats() {
        const provinces = new Set();
        const districts = new Set();
        const subdistricts = new Set();
        const postalCodes = new Set();

        this.data.forEach(item => {
            provinces.add(item.provinceCode);
            districts.add(item.districtCode);
            subdistricts.add(item.subdistrictCode);
            postalCodes.add(item.postalCode);
        });

        return {
            totalRecords: this.data.length,
            provinceCount: provinces.size,
            districtCount: districts.size,
            subdistrictCount: subdistricts.size,
            postalCodeCount: postalCodes.size
        };
    }
}

// Create instance and export
const thailandGeography = new ThailandGeography(geography);

// Export the class and instance (for ES6 modules)
export { ThailandGeography, thailandGeography as default };

// Initialize window objects immediately (for direct script usage)
(function () {
    // Check if window object exists (browser environment)
    if (typeof window !== 'undefined') {
        // Make it globally available through window object
        window.eef = window.eef || {};
        window.eef.ThailandGeography = thailandGeography;
        window.eef.ThailandGeographyClass = ThailandGeography;

        // Also make it available directly on window for easier access
        window.ThailandGeography = thailandGeography;
        window.ThailandGeographyClass = ThailandGeography;

        // Add convenience methods to window.eef
        window.eef.geography = {
            /**
             * Quick access to get all provinces
             * @returns {Array} Array of provinces
             */
            getProvinces: () => thailandGeography.getAllProvinces(),

            /**
             * Quick access to get districts by province
             * @param {number|string} provinceCode - Province code
             * @returns {Array} Array of districts
             */
            getDistricts: (provinceCode) => thailandGeography.getDistrictsByProvince(provinceCode),

            /**
             * Quick access to get subdistricts by district
             * @param {number|string} provinceCode - Province code
             * @param {number|string} districtCode - District code
             * @returns {Array} Array of subdistricts
             */
            getSubdistricts: (provinceCode, districtCode) => thailandGeography.getSubdistrictsByDistrict(provinceCode, districtCode),

            /**
             * Quick search for any location
             * @param {string} searchTerm - Search term
             * @param {string} type - Type: 'province', 'district', or 'all'
             * @returns {Object} Search results
             */
            search: (searchTerm, type = 'all') => {
                const results = {};

                if (type === 'province' || type === 'all') {
                    results.provinces = thailandGeography.searchProvinces(searchTerm);
                }

                if (type === 'all') {
                    results.districts = [];
                    results.subdistricts = [];

                    // Search in all provinces for districts and subdistricts
                    const allProvinces = thailandGeography.getAllProvinces();
                    allProvinces.forEach(province => {
                        const districts = thailandGeography.searchDistricts(province.provinceCode, searchTerm);
                        results.districts.push(...districts);

                        const allDistricts = thailandGeography.getDistrictsByProvince(province.provinceCode);
                        allDistricts.forEach(district => {
                            const subdistricts = thailandGeography.searchSubdistricts(province.provinceCode, district.districtCode, searchTerm);
                            results.subdistricts.push(...subdistricts);
                        });
                    });
                }

                return results;
            },

            /**
             * Get address by postal code
             * @param {number|string} postalCode - Postal code
             * @returns {Array} Array of addresses
             */
            getByPostalCode: (postalCode) => thailandGeography.getAddressByPostalCode(postalCode),

            /**
             * Get complete address information
             * @param {number|string} provinceCode - Province code
             * @param {number|string} districtCode - District code (optional)
             * @param {number|string} subdistrictCode - Subdistrict code (optional)
             * @returns {Object} Address information
             */
            getAddressInfo: (provinceCode, districtCode = null, subdistrictCode = null) =>
                thailandGeography.getAddressInfo(provinceCode, districtCode, subdistrictCode),

            /**
             * Get statistics
             * @returns {Object} Statistics
             */
            getStats: () => thailandGeography.getStats(),

            /**
             * Create new instance with custom data
             * @param {Array} customData - Custom geography data
             * @returns {ThailandGeography} New instance
             */
            createInstance: (customData) => new ThailandGeography(customData),

            /**
             * Find all subdistricts based on province and district information
             * @param {Object} params - Search parameters
             * @param {number|string} params.provinceCode - Province code (required)
             * @param {string} params.provinceName - Province name (Thai or English, optional)
             * @param {number|string} params.districtCode - District code (optional)
             * @param {string} params.districtName - District name (Thai or English, optional)
             * @returns {Array} Array of matching subdistricts
             */
            findSubdistricts: (params) => {
                const { provinceCode, provinceName, districtCode, districtName } = params;

                // If we have both province and district codes, use the existing method
                if (provinceCode && districtCode) {
                    return thailandGeography.getSubdistrictsByDistrict(provinceCode, districtCode);
                }

                // If we only have province code, get all subdistricts in that province
                if (provinceCode && !districtCode) {
                    return thailandGeography.getSubdistrictsByProvince(provinceCode);
                }

                // If we need to find by names
                let targetProvinceCode = provinceCode;
                let targetDistrictCode = districtCode;

                // Find province code by name if not provided
                if (!targetProvinceCode && provinceName) {
                    const provinces = thailandGeography.searchProvinces(provinceName);
                    if (provinces.length > 0) {
                        targetProvinceCode = provinces[0].provinceCode;
                    } else {
                        return []; // Province not found
                    }
                }

                // Find district code by name if not provided
                if (targetProvinceCode && !targetDistrictCode && districtName) {
                    const districts = thailandGeography.searchDistricts(targetProvinceCode, districtName);
                    if (districts.length > 0) {
                        targetDistrictCode = districts[0].districtCode;
                    } else {
                        return []; // District not found
                    }
                }

                // Return results based on what we found
                if (targetProvinceCode && targetDistrictCode) {
                    return thailandGeography.getSubdistrictsByDistrict(targetProvinceCode, targetDistrictCode);
                } else if (targetProvinceCode) {
                    return thailandGeography.getSubdistrictsByProvince(targetProvinceCode);
                }

                return [];
            },

            /**
             * Find districts based on province information
             * @param {Object} params - Search parameters
             * @param {number|string} params.provinceCode - Province code (optional)
             * @param {string} params.provinceName - Province name (Thai or English, optional)
             * @returns {Array} Array of matching districts
             */
            findDistricts: (params) => {
                const { provinceCode, provinceName } = params;

                // If we have province code, use it directly
                if (provinceCode) {
                    return thailandGeography.getDistrictsByProvince(provinceCode);
                }

                // Find province code by name
                if (provinceName) {
                    const provinces = thailandGeography.searchProvinces(provinceName);
                    if (provinces.length > 0) {
                        return thailandGeography.getDistrictsByProvince(provinces[0].provinceCode);
                    }
                }

                return [];
            },

            /**
             * Smart search that can handle various input combinations
             * @param {Object} params - Search parameters
             * @param {string} params.province - Province name or code
             * @param {string} params.district - District name or code (optional)
             * @param {string} params.subdistrict - Subdistrict name or code (optional)
             * @param {string} params.postalCode - Postal code (optional)
             * @returns {Object} Search results with matched data
             */
            smartSearch: (params) => {
                const { province, district, subdistrict, postalCode } = params;

                // Search by postal code first if provided
                if (postalCode) {
                    return {
                        type: 'postalCode',
                        results: thailandGeography.getAddressByPostalCode(postalCode)
                    };
                }

                // Determine if inputs are codes (numbers) or names (strings)
                const isProvinceCode = !isNaN(province) && province;
                const isDistrictCode = !isNaN(district) && district;
                const isSubdistrictCode = !isNaN(subdistrict) && subdistrict;

                let provinceCode = isProvinceCode ? Number(province) : null;
                let districtCode = isDistrictCode ? Number(district) : null;
                let subdistrictCode = isSubdistrictCode ? Number(subdistrict) : null;

                // Find province code if searching by name
                if (!provinceCode && province) {
                    const provinces = thailandGeography.searchProvinces(province);
                    if (provinces.length > 0) {
                        provinceCode = provinces[0].provinceCode;
                    }
                }

                // Find district code if searching by name
                if (provinceCode && !districtCode && district) {
                    const districts = thailandGeography.searchDistricts(provinceCode, district);
                    if (districts.length > 0) {
                        districtCode = districts[0].districtCode;
                    }
                }

                // Find subdistrict code if searching by name
                if (provinceCode && districtCode && !subdistrictCode && subdistrict) {
                    const subdistricts = thailandGeography.searchSubdistricts(provinceCode, districtCode, subdistrict);
                    if (subdistricts.length > 0) {
                        subdistrictCode = subdistricts[0].subdistrictCode;
                    }
                }

                // Return appropriate results based on available data
                if (provinceCode && districtCode && subdistrictCode) {
                    return {
                        type: 'complete',
                        results: [thailandGeography.getAddressInfo(provinceCode, districtCode, subdistrictCode)]
                    };
                } else if (provinceCode && districtCode) {
                    return {
                        type: 'subdistricts',
                        results: thailandGeography.getSubdistrictsByDistrict(provinceCode, districtCode)
                    };
                } else if (provinceCode) {
                    return {
                        type: 'districts',
                        results: thailandGeography.getDistrictsByProvince(provinceCode)
                    };
                }

                return {
                    type: 'notFound',
                    results: []
                };
            }
        };
    }
})();