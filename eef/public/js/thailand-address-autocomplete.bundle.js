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
     * Get all districts in a specific province by name
     */
    getDistrictsByProvince(provinceName) {
        // Find province by name (Thai or English)
        const province = this.getAllProvinces().find(p =>
            p.provinceNameTh === provinceName ||
            p.provinceNameEn === provinceName ||
            p.provinceNameEn.toLowerCase() === provinceName.toLowerCase() ||
            p.provinceNameTh.includes(provinceName)
        );

        if (!province) return [];

        const districts = this.data
            .filter(item => item.provinceCode === province.provinceCode)
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
     * Get subdistricts by province name and/or district name
     */
    getSubdistricts(provinceName, districtName = null) {
        // Find province by name
        const province = this.getAllProvinces().find(p =>
            p.provinceNameTh === provinceName ||
            p.provinceNameEn === provinceName ||
            p.provinceNameEn.toLowerCase() === provinceName.toLowerCase() ||
            p.provinceNameTh.includes(provinceName)
        );

        if (!province) return [];

        let filteredData = this.data.filter(item => item.provinceCode === province.provinceCode);

        // If district name is provided, filter by district
        if (districtName) {
            const district = this.getDistrictsByProvince(provinceName).find(d =>
                d.districtNameTh === districtName ||
                d.districtNameEn === districtName ||
                d.districtNameEn.toLowerCase() === districtName.toLowerCase() ||
                d.districtNameTh.includes(districtName)
            );

            if (!district) return [];

            filteredData = filteredData.filter(item => item.districtCode === district.districtCode);
        }

        return filteredData
            .map(this._formatAddressData)
            .sort((a, b) => a.subdistrictCode - b.subdistrictCode);
    }

    // Backward compatibility
    getSubdistrictsByDistrict(provinceName, districtName) {
        return this.getSubdistricts(provinceName, districtName);
    }

    getSubdistrictsByProvince(provinceName) {
        return this.getSubdistricts(provinceName);
    }

    /**
     * Get postal codes for a specific subdistrict by names
     */
    getPostalCodes(provinceName, districtName, subdistrictName) {
        // Find province by name
        const province = this.getAllProvinces().find(p =>
            p.provinceNameTh === provinceName ||
            p.provinceNameEn === provinceName ||
            p.provinceNameEn.toLowerCase() === provinceName.toLowerCase() ||
            p.provinceNameTh.includes(provinceName)
        );

        if (!province) return [];

        // Find district by name
        const district = this.getDistrictsByProvince(provinceName).find(d =>
            d.districtNameTh === districtName ||
            d.districtNameEn === districtName ||
            d.districtNameEn.toLowerCase() === districtName.toLowerCase() ||
            d.districtNameTh.includes(districtName)
        );

        if (!district) return [];

        // Find subdistrict by name
        const subdistrict = this.getSubdistricts(provinceName, districtName).find(s =>
            s.subdistrictNameTh === subdistrictName ||
            s.subdistrictNameEn === subdistrictName ||
            s.subdistrictNameEn.toLowerCase() === subdistrictName.toLowerCase() ||
            s.subdistrictNameTh.includes(subdistrictName)
        );

        if (!subdistrict) return [];

        return [...new Set(
            this.data
                .filter(item =>
                    item.provinceCode === province.provinceCode &&
                    item.districtCode === district.districtCode &&
                    item.subdistrictCode === subdistrict.subdistrictCode
                )
                .map(item => item.postalCode)
        )].sort();
    }    /**
     * Universal search function
     */
    search(searchTerm, type = 'all', provinceName = null, districtName = null) {
        const results = {};

        if (type === 'province' || type === 'all') {
            results.provinces = this.getAllProvinces().filter(p =>
                this._matchesSearch(p.provinceNameEn, p.provinceNameTh, searchTerm)
            );
        }

        if ((type === 'district' || type === 'all') && provinceName) {
            results.districts = this.getDistrictsByProvince(provinceName).filter(d =>
                this._matchesSearch(d.districtNameEn, d.districtNameTh, searchTerm)
            );
        }

        if ((type === 'subdistrict' || type === 'all') && provinceName && districtName) {
            results.subdistricts = this.getSubdistricts(provinceName, districtName).filter(s =>
                this._matchesSearch(s.subdistrictNameEn, s.subdistrictNameTh, searchTerm)
            );
        }

        return results;
    }

    // Backward compatibility methods
    searchProvinces(searchTerm) {
        return this.search(searchTerm, 'province').provinces || [];
    }

    searchDistricts(provinceName, searchTerm) {
        return this.search(searchTerm, 'district', provinceName).districts || [];
    }

    searchSubdistricts(provinceName, districtName, searchTerm) {
        return this.search(searchTerm, 'subdistrict', provinceName, districtName).subdistricts || [];
    }

    /**
     * Get complete address information by names
     */
    getAddressInfo(provinceName, districtName = null, subdistrictName = null) {
        // Find province by name
        const province = this.getAllProvinces().find(p =>
            p.provinceNameTh === provinceName ||
            p.provinceNameEn === provinceName ||
            p.provinceNameEn.toLowerCase() === provinceName.toLowerCase() ||
            p.provinceNameTh.includes(provinceName)
        );

        if (!province) return null;

        let result = this.data.find(item => item.provinceCode === province.provinceCode);

        if (districtName) {
            const district = this.getDistrictsByProvince(provinceName).find(d =>
                d.districtNameTh === districtName ||
                d.districtNameEn === districtName ||
                d.districtNameEn.toLowerCase() === districtName.toLowerCase() ||
                d.districtNameTh.includes(districtName)
            );

            if (!district) return null;

            result = this.data.find(item =>
                item.provinceCode === province.provinceCode &&
                item.districtCode === district.districtCode
            );

            if (subdistrictName) {
                const subdistrict = this.getSubdistricts(provinceName, districtName).find(s =>
                    s.subdistrictNameTh === subdistrictName ||
                    s.subdistrictNameEn === subdistrictName ||
                    s.subdistrictNameEn.toLowerCase() === subdistrictName.toLowerCase() ||
                    s.subdistrictNameTh.includes(subdistrictName)
                );

                if (!subdistrict) return null;

                result = this.data.find(item =>
                    item.provinceCode === province.provinceCode &&
                    item.districtCode === district.districtCode &&
                    item.subdistrictCode === subdistrict.subdistrictCode
                );
            }
        }

        return result ? this._formatAddressData(result) : null;
    }    /**
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
        getDistrictsByProvince: (provinceName) => thailandGeography.getDistrictsByProvince(provinceName),
        getDistricts: (provinceName) => thailandGeography.getDistrictsByProvince(provinceName),
        getSubdistricts: (provinceName, districtName = null) => thailandGeography.getSubdistricts(provinceName, districtName),
        getByPostalCode: (postalCode) => thailandGeography.getAddressByPostalCode(postalCode),
        getAddressInfo: (provinceName, districtName = null, subdistrictName = null) =>
            thailandGeography.getAddressInfo(provinceName, districtName, subdistrictName),
        getStats: () => thailandGeography.getStats(),
        createInstance: (customData) => new ThailandGeography(customData),

        // Unified search method
        search: (searchTerm, type = 'all', provinceName = null, districtName = null) =>
            thailandGeography.search(searchTerm, type, provinceName, districtName),

        // Smart search with automatic type detection
        smartSearch: (params) => {
            const { province, district, subdistrict, postalCode } = params;

            if (postalCode) {
                return { type: 'postalCode', results: thailandGeography.getAddressByPostalCode(postalCode) };
            }

            // All searches are now by name, no code detection needed
            if (!province) return { type: 'notFound', results: [] };

            // Check if province exists
            const foundProvince = thailandGeography.searchProvinces(province);
            if (!foundProvince.length) return { type: 'notFound', results: [] };

            const provinceName = foundProvince[0].provinceNameTh;

            if (subdistrict && district) {
                const result = thailandGeography.getAddressInfo(provinceName, district, subdistrict);
                return {
                    type: 'complete',
                    results: result ? [result] : []
                };
            } else if (district) {
                return {
                    type: 'subdistricts',
                    results: thailandGeography.getSubdistricts(provinceName, district)
                };
            } else {
                return {
                    type: 'districts',
                    results: thailandGeography.getDistrictsByProvince(provinceName)
                };
            }
        }
    };
}