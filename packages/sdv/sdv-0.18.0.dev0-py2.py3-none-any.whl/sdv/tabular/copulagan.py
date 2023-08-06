"""Combination of GaussianCopula transformation and GANs."""

from rdt import HyperTransformer
from rdt.transformers import GaussianNormalizer

from sdv.tabular.ctgan import CTGAN


class CopulaGAN(CTGAN):
    """Combination of GaussianCopula transformation and GANs.

    This model extends the ``CTGAN`` model to add the flexibility of the GaussianCopula
    transformations provided by the ``GaussianNormalizer`` from ``RDT``.

    Overall, the fitting process consists of the following steps:

    1. Transform each non categorical variable from the input
       data using a ``GaussianNormalizer``:

       i. If not specified, find out the distribution which each one
          of the variables from the input dataset has.
       ii. Transform each variable to a standard normal space by applying
           the CDF of the corresponding distribution and later on applying
           an inverse CDF from a standard normal distribution.

    2. Fit CTGAN with the transformed table.

    And the process of sampling is:

    1. Sample using CTGAN
    2. Reverse the previous transformation by applying the CDF of a standard normal
       distribution and then inverting the CDF of the distribution that correpsonds
       to each variable.

    The arguments of this model are the same as for CTGAN except for two additional
    arguments, ``field_distributions`` and ``default_distribution`` that give the
    ability to define specific transformations for individual fields as well as
    which distribution to use by default if no specific distribution has been selected.

    Distributions can be passed as a ``copulas`` univariate instance or as one
    of the following string values:

    * ``gaussian``: Use a Gaussian distribution.
    * ``gamma``: Use a Gamma distribution.
    * ``beta``: Use a Beta distribution.
    * ``student_t``: Use a Student T distribution.
    * ``gaussian_kde``: Use a GaussianKDE distribution. This model is non-parametric,
      so using this will make ``get_parameters`` unusable.
    * ``truncated_gaussian``: Use a Truncated Gaussian distribution.

    Args:
        field_names (list[str]):
            List of names of the fields that need to be modeled
            and included in the generated output data. Any additional
            fields found in the data will be ignored and will not be
            included in the generated output.
            If ``None``, all the fields found in the data are used.
        field_types (dict[str, dict]):
            Dictinary specifying the data types and subtypes
            of the fields that will be modeled. Field types and subtypes
            combinations must be compatible with the SDV Metadata Schema.
        field_transformers (dict[str, str]):
            Dictinary specifying which transformers to use for each field.
            Available transformers are:

                * ``FloatFormatter``: Uses a ``FloatFormatter`` for numerical data.
                * ``FrequencyEncoder``: Uses a ``FrequencyEncoder`` without gaussian noise.
                * ``FrequencyEncoder_noised``: Uses a ``FrequencyEncoder`` adding gaussian noise.
                * ``OneHotEncoder``: Uses a ``OneHotEncoder``.
                * ``LabelEncoder``: Uses a ``LabelEncoder`` without gaussian nose.
                * ``LabelEncoder_noised``: Uses a ``LabelEncoder`` adding gaussian noise.
                * ``BinaryEncoder``: Uses a ``BinaryEncoder``.
                * ``UnixTimestampEncoder``: Uses a ``UnixTimestampEncoder``.

        anonymize_fields (dict[str, str]):
            Dict specifying which fields to anonymize and what faker
            category they belong to.
        primary_key (str):
            Name of the field which is the primary key of the table.
        constraints (list[Constraint, dict]):
            List of Constraint objects or dicts.
        table_metadata (dict or metadata.Table):
            Table metadata instance or dict representation.
            If given alongside any other metadata-related arguments, an
            exception will be raised.
            If not given at all, it will be built using the other
            arguments or learned from the data.
        log_frequency (boolean):
            Whether to use log frequency of categorical levels in conditional
            sampling. Defaults to ``True``.
        embedding_dim (int):
            Size of the random sample passed to the Generator. Defaults to 128.
        generator_dim (tuple or list of ints):
            Size of the output samples for each one of the Residuals. A Resiudal Layer
            will be created for each one of the values provided. Defaults to (256, 256).
        discriminator_dim (tuple or list of ints):
            Size of the output samples for each one of the Discriminator Layers. A Linear
            Layer will be created for each one of the values provided. Defaults to (256, 256).
        batch_size (int):
            Number of data samples to process in each step.
        verbose (bool):
            Whether to print fit progress on stdout. Defaults to ``False``.
        epochs (int):
            Number of training epochs. Defaults to 300.
        cuda (bool or str):
            If ``True``, use CUDA. If an ``str``, use the indicated device.
            If ``False``, do not use cuda at all.
        field_distributions (dict):
            Optionally specify a dictionary that maps the name of each field to the distribution
            that must be used in it. Fields that are not specified in the input ``dict`` will
            be modeled using the default distribution. Defaults to ``None``.
        default_distribution (copulas.univariate.Univariate or str):
            Distribution to use on the fields for which no specific distribution has been given.
            Defaults to ``truncated_gaussian``.
        learn_rounding_scheme (bool):
            Define rounding scheme for ``FloatFormatter``. If ``True``, the data returned by
            ``reverse_transform`` will be rounded to that place. Defaults to ``True``.
        enforce_min_max_values (bool):
            Specify whether or not to clip the data returned by ``reverse_transform`` of
            the numerical transformer, ``FloatFormatter``, to the min and max values seen
            during ``fit``. Defaults to ``True``.
    """

    DEFAULT_DISTRIBUTION = 'truncated_gaussian'
    _field_distributions = None
    _default_distribution = None
    _hyper_transformer = None

    def __init__(self, field_names=None, field_types=None, field_transformers=None,
                 anonymize_fields=None, primary_key=None, constraints=None, table_metadata=None,
                 embedding_dim=128, generator_dim=(256, 256), discriminator_dim=(256, 256),
                 generator_lr=2e-4, generator_decay=1e-6, discriminator_lr=2e-4,
                 discriminator_decay=1e-6, batch_size=500, discriminator_steps=1,
                 log_frequency=True, verbose=False, epochs=300, cuda=True,
                 field_distributions=None, default_distribution=None, learn_rounding_scheme=True,
                 enforce_min_max_values=True):
        super().__init__(
            field_names=field_names,
            primary_key=primary_key,
            field_types=field_types,
            field_transformers=field_transformers,
            anonymize_fields=anonymize_fields,
            constraints=constraints,
            table_metadata=table_metadata,
            embedding_dim=embedding_dim,
            generator_dim=generator_dim,
            discriminator_dim=discriminator_dim,
            generator_lr=generator_lr,
            generator_decay=generator_decay,
            discriminator_lr=discriminator_lr,
            discriminator_decay=discriminator_decay,
            batch_size=batch_size,
            discriminator_steps=discriminator_steps,
            log_frequency=log_frequency,
            verbose=verbose,
            epochs=epochs,
            cuda=cuda,
            learn_rounding_scheme=learn_rounding_scheme,
            enforce_min_max_values=enforce_min_max_values,
        )
        self._field_distributions = field_distributions or dict()
        self._default_distribution = default_distribution or self.DEFAULT_DISTRIBUTION

    def get_distributions(self):
        """Get the marginal distributions used by this CopulaGAN.

        Returns:
            dict:
                Dictionary containing the distributions used or detected
                for each column.
        """
        return {
            transformer.column_prefix: transformer._univariate.to_dict()['type']
            for transformer in self._hyper_transformer._transformers_sequence
            if isinstance(transformer, GaussianNormalizer)
        }

    def _fit(self, table_data):
        """Fit the model to the table.

        Args:
            table_data (pandas.DataFrame):
                Data to be learned.
        """
        distributions = self._field_distributions
        fields = self._metadata.get_fields()

        sdtypes = {}
        transformers = {}
        for field in table_data:
            field_sdtype = fields.get(field, {}).get('type')
            if field in fields and field_sdtype != 'categorical':
                sdtypes[field] = 'numerical'
                transformers[field] = GaussianNormalizer(
                    model_missing_values=True,
                    distribution=distributions.get(field, self._default_distribution)
                )
            else:
                sdtypes[field] = field_sdtype or 'categorical'
                transformers[field] = None

        self._hyper_transformer = HyperTransformer()
        self._hyper_transformer.set_config({'transformers': transformers, 'sdtypes': sdtypes})
        table_data = self._hyper_transformer.fit_transform(table_data[list(transformers)])

        super()._fit(table_data)

    def _sample(self, num_rows, conditions=None):
        """Sample the indicated number of rows from the model.

        Args:
            num_rows (int):
                Amount of rows to sample.
            conditions (dict):
                If specified, this dictionary maps column names to the column
                value. Then, this method generates `num_rows` samples, all of
                which are conditioned on the given variables.

        Returns:
            pandas.DataFrame:
                Sampled data.
        """
        sampled = super()._sample(num_rows, conditions)
        return self._hyper_transformer.reverse_transform(sampled)
