# axidraw modular service

This module implements the [rdk gantry API](https://github.com/rdk/gantry-api) in a jalen:viam-axidraw:axidraw model.
With this model, you can...

## Requirements

_Add instructions here for any requirements._

``` bash
```

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `rdk:gantry:jalen:viam-axidraw:axidraw` model from the [`jalen:viam-axidraw:axidraw` module](https://app.viam.com/module/rdk/jalen:viam-axidraw:axidraw).

## Configure your gantry

> [!NOTE]  
> Before configuring your gantry, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**.
Select the `gantry` type, then select the `jalen:viam-axidraw:axidraw` model. 
Enter a name for your gantry and click **Create**.

On the new component panel, copy and paste the following attribute template into your gantry’s **Attributes** box:

```json
{
  TODO: INSERT SAMPLE ATTRIBUTES
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `rdk:gantry:jalen:viam-axidraw:axidraw` gantrys:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `todo1` | string | **Required** |  TODO |
| `todo2` | string | Optional |  TODO |

### Example Configuration

```json
{
  TODO: INSERT SAMPLE CONFIGURATION(S)
}
```

### Next Steps

_Add any additional information you want readers to know and direct them towards what to do next with this module._
_For example:_ 

- To test your...
- To write code against your...

## Troubleshooting

_Add troubleshooting notes here._
