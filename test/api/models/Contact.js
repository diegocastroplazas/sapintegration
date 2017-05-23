/**
 * Contact.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {



  attributes: {
      number: {
          required: true,
          type: 'string',
          unique: true
      },
      firstName: {
          required: true,
          type: 'string'
      },
      companyName: {
          required: true,
          type: 'string'
      },
      nitNumber: {
          required: true,
          type: 'string'
      }
  }
};
