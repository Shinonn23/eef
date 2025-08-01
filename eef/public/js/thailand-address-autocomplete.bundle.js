import geography from "./geography.json"

/**
 * Thailand Geography Data Helper
 * Optimized version with reduced code duplication
 */
class ThailandGeography {
    constructor(data) {
        this.data = data;
    }

    // Helper function to format address data
    _formatAddressData(item) {
        return {
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
        };
    }

    // Helper function for unique filtering
    _getUnique(items, keyField, sortField) {
        const unique = new Map();
        items.forEach(item => {
            if (!unique.has(item[keyField])) {
                unique.set(item[keyField], item);
            }
        });
        return Array.from(unique.values()).sort((a, b) => a[sortField] - b[sortField]);
    }

    // Helper function for search matching
    _matchesSearch(nameEn, nameTh, searchTerm) {
        const term = searchTerm.toLowerCase();
        return nameEn.toLowerCase().includes(term) || nameTh.includes(searchTerm);
    }

    /**
     * Get all provinces in Thailand
     */
    getAllProvinces() {
        const provinces = this.data.map(item => ({
            provinceCode: item.provinceCode,
            provinceNameEn: item.provinceNameEn,
            provinceNameTh: item.provinceNameTh
        }));
        return this._getUnique(provinces, 'provinceCode', 'provinceCode');
    }

    /**
     * Get all districts in a specific province
     */
    getDistrictsByProvince(provinceCode) {
        const numProvinceCode = Number(provinceCode);
        const districts = this.data
            .filter(item => item.provinceCode === numProvinceCode)
            .map(item => ({
                provinceCode: item.provinceCode,
                provinceNameEn: item.provinceNameEn,
                provinceNameTh: item.provinceNameTh,
                districtCode: item.districtCode,
                districtNameEn: item.districtNameEn,
                districtNameTh: item.districtNameTh
            }));
        return this._getUnique(districts, 'districtCode', 'districtCode');
    }

    /**
     * Get subdistricts by province and/or district
     */
    getSubdistricts(provinceCode, districtCode = null) {
        const numProvinceCode = Number(provinceCode);
        const numDistrictCode = districtCode ? Number(districtCode) : null;

        return this.data
            .filter(item => {
                if (numDistrictCode) {
                    return item.provinceCode === numProvinceCode && item.districtCode === numDistrictCode;
                }
                return item.provinceCode === numProvinceCode;
            })
            .map(this._formatAddressData)
            .sort((a, b) => a.subdistrictCode - b.subdistrictCode);
    }

    // Backward compatibility
    getSubdistrictsByDistrict(provinceCode, districtCode) {
        return this.getSubdistricts(provinceCode, districtCode);
    }

    getSubdistrictsByProvince(provinceCode) {
        return this.getSubdistricts(provinceCode);
    }

    /**
     * Get postal codes for a specific subdistrict
     */
    getPostalCodes(provinceCode, districtCode, subdistrictCode) {
        return [...new Set(
            this.data
                .filter(item =>
                    item.provinceCode === Number(provinceCode) &&
                    item.districtCode === Number(districtCode) &&
                    item.subdistrictCode === Number(subdistrictCode)
                )
                .map(item => item.postalCode)
        )].sort();
    }

    /**
     * Universal search function
     */
    search(searchTerm, type = 'all', provinceCode = null, districtCode = null) {
        const results = {};

        if (type === 'province' || type === 'all') {
            results.provinces = this.getAllProvinces().filter(p =>
                this._matchesSearch(p.provinceNameEn, p.provinceNameTh, searchTerm)
            );
        }

        if ((type === 'district' || type === 'all') && provinceCode) {
            results.districts = this.getDistrictsByProvince(provinceCode).filter(d =>
                this._matchesSearch(d.districtNameEn, d.districtNameTh, searchTerm)
            );
        }

        if ((type === 'subdistrict' || type === 'all') && provinceCode && districtCode) {
            results.subdistricts = this.getSubdistricts(provinceCode, districtCode).filter(s =>
                this._matchesSearch(s.subdistrictNameEn, s.subdistrictNameTh, searchTerm)
            );
        }

        return results;
    }

    // Backward compatibility methods
    searchProvinces(searchTerm) {
        return this.search(searchTerm, 'province').provinces || [];
    }

    searchDistricts(provinceCode, searchTerm) {
        return this.search(searchTerm, 'district', provinceCode).districts || [];
    }

    searchSubdistricts(provinceCode, districtCode, searchTerm) {
        return this.search(searchTerm, 'subdistrict', provinceCode, districtCode).subdistricts || [];
    }

    /**
     * Get complete address information by codes
     */
    getAddressInfo(provinceCode, districtCode = null, subdistrictCode = null) {
        const result = this.data.find(item => {
            if (subdistrictCode) {
                return item.provinceCode === Number(provinceCode) &&
                    item.districtCode === Number(districtCode) &&
                    item.subdistrictCode === Number(subdistrictCode);
            }
            if (districtCode) {
                return item.provinceCode === Number(provinceCode) &&
                    item.districtCode === Number(districtCode);
            }
            return item.provinceCode === Number(provinceCode);
        });

        return result ? this._formatAddressData(result) : null;
    }

    /**
     * Find addresses by postal code
     */
    getAddressByPostalCode(postalCode) {
        return this.data
            .filter(item => item.postalCode === Number(postalCode))
            .map(this._formatAddressData);
    }

    /**
     * Get statistics about the geography data
     */
    getStats() {
        const stats = { provinces: new Set(), districts: new Set(), subdistricts: new Set(), postalCodes: new Set() };

        this.data.forEach(item => {
            stats.provinces.add(item.provinceCode);
            stats.districts.add(item.districtCode);
            stats.subdistricts.add(item.subdistrictCode);
            stats.postalCodes.add(item.postalCode);
        });

        return {
            totalRecords: this.data.length,
            provinceCount: stats.provinces.size,
            districtCount: stats.districts.size,
            subdistrictCount: stats.subdistricts.size,
            postalCodeCount: stats.postalCodes.size
        };
    }
}

// Create instance and export
const thailandGeography = new ThailandGeography(geography);
export { ThailandGeography, thailandGeography as default };

// Browser environment setup
if (typeof window !== 'undefined') {
    // Setup window objects
    window.eef = window.eef || {};
    Object.assign(window.eef, {
        ThailandGeography: thailandGeography,
        ThailandGeographyClass: ThailandGeography
    });

    // Direct window access
    window.ThailandGeography = thailandGeography;
    window.ThailandGeographyClass = ThailandGeography;

    // Simplified convenience API
    window.eef.geography = {
        // Direct method proxies
        getProvinces: () => thailandGeography.getAllProvinces(),
        getDistricts: (provinceCode) => thailandGeography.getDistrictsByProvince(provinceCode),
        getSubdistricts: (provinceCode, districtCode = null) => thailandGeography.getSubdistricts(provinceCode, districtCode),
        getByPostalCode: (postalCode) => thailandGeography.getAddressByPostalCode(postalCode),
        getAddressInfo: (provinceCode, districtCode = null, subdistrictCode = null) =>
            thailandGeography.getAddressInfo(provinceCode, districtCode, subdistrictCode),
        getStats: () => thailandGeography.getStats(),
        createInstance: (customData) => new ThailandGeography(customData),

        // Unified search method
        search: (searchTerm, type = 'all', provinceCode = null, districtCode = null) =>
            thailandGeography.search(searchTerm, type, provinceCode, districtCode),

        // Smart search with automatic type detection
        smartSearch: (params) => {
            const { province, district, subdistrict, postalCode } = params;

            if (postalCode) {
                return { type: 'postalCode', results: thailandGeography.getAddressByPostalCode(postalCode) };
            }

            // Auto-detect codes vs names
            const provinceCode = !isNaN(province) ? Number(province) :
                (() => {
                    const found = thailandGeography.searchProvinces(province);
                    return found.length ? found[0].provinceCode : null;
                })();

            if (!provinceCode) return { type: 'notFound', results: [] };

            const districtCode = !isNaN(district) ? Number(district) :
                district ? (() => {
                    const found = thailandGeography.searchDistricts(provinceCode, district);
                    return found.length ? found[0].districtCode : null;
                })() : null;

            const subdistrictCode = !isNaN(subdistrict) ? Number(subdistrict) :
                (districtCode && subdistrict) ? (() => {
                    const found = thailandGeography.searchSubdistricts(provinceCode, districtCode, subdistrict);
                    return found.length ? found[0].subdistrictCode : null;
                })() : null;

            if (subdistrictCode) {
                return {
                    type: 'complete',
                    results: [thailandGeography.getAddressInfo(provinceCode, districtCode, subdistrictCode)]
                };
            } else if (districtCode) {
                return {
                    type: 'subdistricts',
                    results: thailandGeography.getSubdistricts(provinceCode, districtCode)
                };
            } else {
                return {
                    type: 'districts',
                    results: thailandGeography.getDistrictsByProvince(provinceCode)
                };
            }
        }
    };
}