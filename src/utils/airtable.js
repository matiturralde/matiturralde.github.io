var Airtable = require('airtable');
var _ = require('lodash');

// Start AirPromise
var AirPromise = function (config) {
    this._airpromise = new Airtable(config);
};

AirPromise.prototype.base = function (baseId) {
    return new AirPromiseBase(this._airpromise, baseId);
};

var AirPromiseBase = function (conn, baseId) {
    this._base = conn.base(baseId);
};

AirPromiseBase.prototype = {
    table: function (tableName) {
        return new AirPromiseTable(this._base, tableName);
    }
};

var AirPromiseTable = function (base, tableName) {
    this._base = base;
    this._table = base(tableName);
};

AirPromiseTable.prototype = {
    populate: function (record, config) {
        var that = this;
        var populateKeys = Object.keys(config);
        var fields = record.fields;

        var promises = populateKeys.map(function (k) {
            var keyConfig = config[k];
            var idsToPopulate = fields[k];
            var tableName = keyConfig.table || keyConfig;

            if (!idsToPopulate || !idsToPopulate.length) {
                return Promise.resolve({});
            }

            var formula = 'OR(' + idsToPopulate.map(function (field) {
                return 'RECORD_ID() = "' + field + '"';
            }).join(',') + ')';

            var table = new AirPromiseTable(that._base, tableName);
            var query = {
                filterByFormula: formula,
                populate: keyConfig.populate || null
            };
            return table.selectFirstPage(query);
        });


        return Promise.all(promises).then(function (responses) {

            populateKeys.forEach(function (k, i) {
                if (responses[i].length) {
                    fields[k] = responses[i].map(function (expanded) {
                        return _.assign(expanded.fields, {
                            _id: expanded.id
                        });
                    });
                }
            });

            return record;
        });
    },
    getByIds: function (ids) {
        ids = ids || [];
        var formula = 'OR(' + ids.map(function (id) {
            return 'RECORD_ID() = "' + id + '"';
        }).join(',') + ')';

        return this.selectAllByFormula(formula);
    },
    find: function (query, options) {
        var that = this;
        return new Promise(function (resolve, reject) {
            that._table.find(query, function (err, record) {
                if (err) {
                    reject(err);
                } else {
                    if (options && options.populate) {
                        that.populate(record, options.populate).then(resolve);
                    } else {
                        resolve(record);
                    }
                }
            });
        });
    },
    select: function (query) {
        return this._table.select(query);
    },
    update: function (id, query) {
        var that = this;
        return new Promise(function (resolve, reject) {
            that._table.update(id, query, function (err, record) {
                err ? reject(err) : resolve(record);
            });
        });
    },
    selectFirstPage: function (query) {
        var that = this;
        query = _.defaults(query, {
            maxRecords: 1000
        });

        return new Promise(function (resolve, reject) {
            that.select(query).firstPage(function (err, records) {
                if (err) {
                    reject(err);
                } else {
                    if (query.populate) {
                        Promise.all(records.map(function (record) {
                            return that.populate(record, query.populate);
                        })).then(resolve);
                    } else {
                        resolve(records);
                    }
                }
            });
        });
    },
    selectAll: function (query) {
        var that = this;

        return new Promise(function (resolve, reject) {
            var all = [];
            that.select(query || {}).eachPage(function (records, next) {
                all = all.concat(records);
                next();
            }, function (err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(all);
                }
            });
        });
    },
    selectOne: function (query) {
        var that = this;

        return that.selectFirstPage(query).then(function (records) {
            return records[0];
        });
    },
    selectAllByFormula: function (formula) {
        return this.selectAll({
            filterByFormula: formula
        });
    },
    selectOneByFormula: function (formula) {
        return this.selectOne({
            filterByFormula: formula
        });
    },
    create: function (newRecord) {
        var that = this;
        return new Promise(function (resolve, reject) {
            that._table.create(newRecord, function (err, record) {
                if (err) {
                    reject(err);
                } else {
                    resolve(record);
                }
            });
        });
    }
};
// End AirPromise

module.exports = new AirPromise({
    apiKey: 'keyJirfxPJNxhZa6i'
});