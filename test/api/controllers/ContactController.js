/**
 * ContactController
 *
 * @description :: Server-side logic for managing contacts
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {
	getCostumerInfo: function (req, res) {
		var dataFromDevice = req.params.all();
		Contact.find({number:dataFromDevice.phoneNumber})
		.exec(function (err, Finn) {
			if (err) {
				console.log("No se encontro el usuario");
				console.log(err);
				return res.serverError(err);
			}
			console.log("usuario encontrado: ");
			return res.json(Finn);
		})
	}

};
